import json
from functools import lru_cache
from typing import List, Optional
from urllib.parse import urlparse, urlunparse

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AWEN_", case_sensitive=False, env_file=".env")

    project_name: str = "AWEN API"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    secret_key: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    upload_dir: str = "uploads"
    rate_limit_max: int = 100
    rate_limit_window: int = 60

    # Storage (Vercel Blob / S3-compatible)
    storage_provider: str = "vercel-blob"
    blob_read_write_token: str = ""
    storage_bucket: str = "awen-uploads"
    storage_region: str = "auto"
    storage_access_key: str = ""
    storage_secret_key: str = ""
    storage_endpoint_url: str = ""
    storage_presigned_ttl: int = 3600
    upload_max_size: int = 10485760  # 10MB
    upload_allowed_types: List[str] = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
    ]

    database_url: str = "postgresql+psycopg://postgres:CHANGE_ME@localhost:5432/awen_db"

    # Supabase (inyectado por Vercel Marketplace)
    supabase_url: str = Field(default="", alias="SUPABASE_URL")
    supabase_anon_key: str = Field(default="", alias="NEXT_PUBLIC_SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(default="", alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_jwt_secret: str = Field(default="", alias="SUPABASE_JWT_SECRET")

    # Database URL con pooler (inyectado por Vercel Marketplace)
    postgres_url: str = Field(default="", alias="POSTGRES_URL")
    postgres_url_no_ssl: str = Field(default="", alias="POSTGRES_URL_NO_SSL")
    postgres_prisma_url: str = Field(default="", alias="POSTGRES_PRISMA_URL")

    # Supabase Storage (opcional, para reemplazar Vercel Blob)
    supabase_storage_bucket: str = Field(default="awen-uploads", alias="SUPABASE_STORAGE_BUCKET")

    @field_validator("upload_allowed_types", mode="before")
    @classmethod
    def parse_upload_allowed_types(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [t.strip() for t in v.split(",") if t.strip()]
        return v
    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    nominatim_reverse_url: str = "https://nominatim.openstreetmap.org/reverse"
    nominatim_user_agent: str = "AWEN-Tracking"
    nominatim_timeout_seconds: float = 6.0
    osrm_url: str = "https://router.project-osrm.org/route/v1/driving"
    osrm_timeout_seconds: float = 6.0

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("secret_key", mode="after")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        if v == "CHANGE_ME":
            raise ValueError(
                "AWEN_SECRET_KEY no puede ser el valor por defecto 'CHANGE_ME'. "
                "Configure una clave secreta segura en la variable de entorno AWEN_SECRET_KEY."
            )
        return v

    @staticmethod
    def _normalize_database_url(url: str) -> str:
        """
        Normaliza una URL de PostgreSQL para el driver async psycopg.

        - `postgres://` -> `postgresql+psycopg://`
        - `postgresql://` -> `postgresql+psycopg://`
        - elimina parametros exclusivos de Prisma/pgBouncer que psycopg no reconoce.
        """
        if not url:
            return url
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://") :]
        if url.startswith("postgresql://"):
            url = "postgresql+psycopg://" + url[len("postgresql://") :]

        parsed = urlparse(url)
        if parsed.query:
            blocked = {"pgbouncer", "connection_limit", "pool_timeout"}
            kept = [
                item
                for item in parsed.query.split("&")
                if item.split("=", 1)[0] not in blocked
            ]
            url = urlunparse(parsed._replace(query="&".join(kept)))
        return url

    @property
    def effective_database_url(self) -> str:
        """Retorna la URL de base de datos efectiva (Postgres URL con pooler si esta disponible)."""
        if self.postgres_url:
            return self._normalize_database_url(self.postgres_url)
        if self.postgres_url_no_ssl:
            return self._normalize_database_url(self.postgres_url_no_ssl)
        return self._normalize_database_url(self.database_url)


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
