from functools import lru_cache
from typing import List, Any, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

import json

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AWEN_", case_sensitive=False, env_file=".env")

    project_name: str = "AWEN API"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    secret_key: str = "password"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    upload_dir: str = "uploads"
    rate_limit_max: int = 100
    rate_limit_window: int = 60
    database_url: str = "postgresql+psycopg://ali_dev:password@localhost:5432/awen_db"
    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    nominatim_reverse_url: str = "https://nominatim.openstreetmap.org/reverse"
    nominatim_user_agent: str = "AWEN-Tracking"
    nominatim_timeout_seconds: float = 6.0
    osrm_url: str = "https://router.project-osrm.org/route/v1/driving"
    osrm_timeout_seconds: float = 6.0

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any):
        if isinstance(v, str):
            # 1. Try to parse as JSON if it looks like a list
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            
            # Otherwise, treat as comma-separated string
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        
        return v


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
