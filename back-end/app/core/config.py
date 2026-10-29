import json
from functools import lru_cache
from typing import List

from pydantic import field_validator
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


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
