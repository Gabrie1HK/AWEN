from __future__ import annotations

import io
import os
import uuid
from typing import BinaryIO, Optional

import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

from app.core.config import get_settings


class StorageService:
    """
    Servicio de almacenamiento compatible con S3 (Vercel Blob, AWS S3, R2, MinIO, etc.).

    Usa pre-signed URLs para subida directa (cliente -> bucket) y descarga.
    """

    def __init__(
        self,
        bucket: Optional[str] = None,
        region: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> None:
        settings = get_settings()

        self._bucket = bucket or settings.storage_bucket
        self._region = region or settings.storage_region
        self._access_key = access_key or settings.storage_access_key
        self._secret_key = secret_key or settings.storage_secret_key
        self._endpoint_url = endpoint_url or settings.storage_endpoint_url
        self._provider = provider or settings.storage_provider
        self._presigned_ttl = settings.storage_presigned_ttl
        self._max_size = settings.upload_max_size
        self._allowed_types = set(settings.upload_allowed_types)

        # Determinar addressing style: path-style para moto/local, virtual para AWS/producción
        is_local = bool(self._endpoint_url and ("localhost" in self._endpoint_url or "127.0.0.1" in self._endpoint_url))
        addressing_style = "path" if is_local or self._provider == "vercel-blob" else "virtual"

        # Cliente S3 (compatible con Vercel Blob, AWS S3, R2, MinIO, moto)
        self._client = boto3.client(
            "s3",
            region_name=self._region if self._region != "auto" else "us-east-1",
            aws_access_key_id=self._access_key or None,
            aws_secret_access_key=self._secret_key or None,
            endpoint_url=self._endpoint_url or None,
            config=BotoConfig(
                s3={"addressing_style": addressing_style},
                signature_version="s3v4",
            ),
        )

        # Para Vercel Blob, el token se usa como access_key
        if self._provider == "vercel-blob" and settings.blob_read_write_token:
            self._client = boto3.client(
                "s3",
                region_name="us-east-1",
                aws_access_key_id=settings.blob_read_write_token,
                aws_secret_access_key="",  # Vercel Blob no usa secret key
                endpoint_url="https://blob.vercel-storage.com",
                config=BotoConfig(
                    s3={"addressing_style": "path"},  # Vercel Blob usa path-style
                    signature_version="s3v4",
                ),
            )

    def validate_file(self, file: BinaryIO, content_type: str, filename: str) -> None:
        """Valida archivo antes de subir."""
        # Verificar tipo
        if content_type not in self._allowed_types:
            raise ValueError(f"Tipo de archivo no permitido: {content_type}")

        # Verificar tamaño (seek al final para obtener tamaño)
        current_pos = file.tell()
        file.seek(0, io.SEEK_END)
        size = file.tell()
        file.seek(current_pos)

        if size == 0:
            raise ValueError("Archivo vacío")
        if size > self._max_size:
            raise ValueError(f"Archivo demasiado grande (máx {self._max_size} bytes)")

    def _generate_key(self, file_type: str, original_filename: str) -> str:
        """Genera key única en bucket: evidence/{type}/{uuid}.ext"""
        ext = os.path.splitext(original_filename)[1].lower()
        if not ext:
            ext = ".bin"
        return f"evidence/{file_type}/{uuid.uuid4().hex}{ext}"

    def generate_presigned_put_url(
        self,
        key: str,
        content_type: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """
        Genera pre-signed URL para PUT (subida directa cliente -> bucket).

        Args:
            key: Key en el bucket
            content_type: MIME type del archivo
            expires_in: Expiración en segundos (default: config TTL)

        Returns:
            URL pre-firmada para PUT
        """
        expires_in = expires_in or self._presigned_ttl
        try:
            url = self._client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )
            return url
        except ClientError as e:
            raise RuntimeError(f"Error generando pre-signed PUT URL: {e}") from e

    def generate_presigned_get_url(
        self,
        key: str,
        expires_in: Optional[int] = None,
    ) -> str:
        """
        Genera pre-signed URL para GET (descarga/visualización).

        Args:
            key: Key en el bucket
            expires_in: Expiración en segundos (default: config TTL)

        Returns:
            URL pre-firmada para GET
        """
        expires_in = expires_in or self._presigned_ttl
        try:
            url = self._client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self._bucket,
                    "Key": key,
                },
                ExpiresIn=expires_in,
            )
            return url
        except ClientError as e:
            raise RuntimeError(f"Error generando pre-signed GET URL: {e}") from e

    def upload_fileobj(
        self,
        fileobj: BinaryIO,
        key: str,
        content_type: str,
    ) -> str:
        """
        Sube archivo vía streaming (backend -> bucket).
        Para archivos grandes o cuando pre-signed PUT no es viable.
        """
        try:
            self._client.upload_fileobj(
                fileobj,
                self._bucket,
                key,
                ExtraArgs={"ContentType": content_type},
            )
            return key
        except ClientError as e:
            raise RuntimeError(f"Error subiendo archivo: {e}") from e

    def upload_bytes(self, data: bytes, key: str, content_type: str) -> str:
        """Sube bytes directamente."""
        fileobj = io.BytesIO(data)
        return self.upload_fileobj(fileobj, key, content_type)

    def delete_file(self, key: str) -> None:
        """Elimina archivo del bucket."""
        try:
            self._client.delete_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            # Si no existe, no es error
            if e.response["Error"]["Code"] != "404":
                raise RuntimeError(f"Error eliminando archivo: {e}") from e

    def file_exists(self, key: str) -> bool:
        """Verifica si archivo existe en bucket."""
        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_file_size(self, key: str) -> Optional[int]:
        """Obtiene tamaño de archivo en bytes."""
        try:
            response = self._client.head_object(Bucket=self._bucket, Key=key)
            return response.get("ContentLength")
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None
            raise