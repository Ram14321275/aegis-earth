from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    service_name: str = Field(default="Aegis Earth", alias="AEGIS_SERVICE_NAME")
    api_version: str = Field(default="v1", alias="AEGIS_API_VERSION")
    environment: str = Field(default="development", alias="AEGIS_ENV")
    log_level: str = Field(default="INFO", alias="AEGIS_LOG_LEVEL")
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
        ],
        alias="AEGIS_CORS_ORIGINS",
    )
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/aegis_earth",
        alias="DATABASE_URL",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

