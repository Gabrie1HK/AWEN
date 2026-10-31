from __future__ import annotations

import os
import uuid
from typing import Optional

import httpx

from app.core.config import get_settings


class SupabaseStorageService:
    """
    Almacenamiento sobre Supabase Storage.

    Usa la Storage API (`/storage/v1`) con la `service_role` key para operaciones
    privadas (subir, borrar, firmar) y URLs publicas para lectura cuando el bucket
    es publico.
    """

    def __init__(
        self,
        bucket: Optional[str] = None,
        supabase_url: Optional[str] = None,
        service_role_key: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        settings = get_settings()

        self._bucket = bucket or settings.supabase_storage_bucket
        self._supabase_url = (supabase_url or settings.supabase_url).rstrip("/")
        self._service_role_key = service_role_key or settings.supabase_service_role_key
        self._max_size = settings.upload_max_size
        self._allowed_types = set(settings.upload_allowed_types)
        self._timeout = timeout

    # ------------------------------------------------------------------ helpers

    def _headers(self, content_type: Optional[str] = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self._service_role_key}",
            "apikey": self._service_role_key,
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=self._timeout)

    def _validate_file(self, size: int, content_type: str) -> None:
        if content_type and content_type not in self._allowed_types:
            raise ValueError(f"Tipo de archivo no permitido: {content_type}")
        if self._max_size and size > self._max_size:
            raise ValueError(f"Archivo demasiado grande (max {self._max_size} bytes)")

    def _generate_key(self, file_type: str, original_filename: str) -> str:
        ext = os.path.splitext(original_filename)[1].lower() or ".bin"
        return f"evidence/{file_type}/{uuid.uuid4().hex}{ext}"

    def _public_url(self, key: str) -> str:
        return f"{self._supabase_url}/storage/v1/object/public/{self._bucket}/{key}"

    # ------------------------------------------------------------------- public

    async def upload_file(
        self,
        content: bytes,
        file_type: str,
        original_filename: str,
        content_type: str,
    ) -> dict:
        """Sube un archivo y devuelve filename, url publica y tamano."""
        self._validate_file(len(content), content_type)
        key = self._generate_key(file_type, original_filename)

        url = f"{self._supabase_url}/storage/v1/object/{self._bucket}/{key}"
        async with self._client() as client:
            response = await client.post(
                url,
                content=content,
                headers=self._headers(content_type),
            )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Error subiendo a Supabase Storage: {response.text}")

        return {"filename": key, "url": self._public_url(key), "size": len(content)}

    async def generate_presigned_put_url(
        self,
        key: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """Firma una URL de subida directa cliente -> bucket."""
        url = f"{self._supabase_url}/storage/v1/object/upload/sign/{self._bucket}/{key}"
        async with self._client() as client:
            response = await client.post(
                url,
                json={"expiresIn": expires_in or 3600},
                headers=self._headers("application/json"),
            )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Error generando URL de subida: {response.text}")

        data = response.json()
        signed = data.get("url") or data.get("signedURL") or data.get("signedUrl") or ""
        if signed.startswith("http"):
            return signed
        token = data.get("token")
        base = f"{self._supabase_url}{signed}"
        return f"{base}?token={token}" if token else base

    async def generate_presigned_get_url(
        self,
        key: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """Firma una URL de descarga. Si el bucket es publico, esto ya sirve."""
        if not expires_in:
            return self._public_url(key)

        url = f"{self._supabase_url}/storage/v1/object/sign/{self._bucket}/{key}"
        async with self._client() as client:
            response = await client.post(
                url,
                json={"expiresIn": expires_in},
                headers=self._headers("application/json"),
            )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Error generando URL de descarga: {response.text}")

        data = response.json()
        signed = data.get("signedURL") or data.get("signedUrl") or data.get("url") or ""
        if signed.startswith("http"):
            return signed
        return f"{self._supabase_url}{signed}"

    async def delete_file(self, key: str) -> None:
        """Elimina un archivo. Un 404 se considera exito (idempotente)."""
        url = f"{self._supabase_url}/storage/v1/object/{self._bucket}/{key}"
        async with self._client() as client:
            response = await client.delete(url, headers=self._headers())

        if response.status_code not in (200, 204, 404):
            raise RuntimeError(f"Error eliminando archivo: {response.text}")

    async def file_exists(self, key: str) -> bool:
        url = f"{self._supabase_url}/storage/v1/object/{self._bucket}/{key}"
        try:
            async with self._client() as client:
                response = await client.head(url, headers=self._headers())
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    async def get_file_size(self, key: str) -> Optional[int]:
        url = f"{self._supabase_url}/storage/v1/object/{self._bucket}/{key}"
        try:
            async with self._client() as client:
                response = await client.head(url, headers=self._headers())
            if response.status_code == 200:
                length = response.headers.get("Content-Length")
                return int(length) if length else None
        except (httpx.HTTPError, ValueError):
            pass
        return None

    async def close(self) -> None:
        """Sin cliente persistente: cada operacion abre y cierra el suyo."""
        return None
