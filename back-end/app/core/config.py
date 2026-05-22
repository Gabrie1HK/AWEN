from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AWEN_", case_sensitive=False)

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
    database_url: str = "postgresql+psycopg://postgres:CHANGE_ME@localhost:5432/awen_db"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
