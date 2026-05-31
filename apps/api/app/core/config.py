from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aegis_env: str = Field(default="development", alias="AEGIS_ENV")
    database_url: str = Field(
        default="postgresql+psycopg://aegis:aegis@localhost:5432/aegis_earth",
        alias="DATABASE_URL",
    )
    open_meteo_base_url: str = Field(default="https://api.open-meteo.com/v1", alias="OPEN_METEO_BASE_URL")
    sentinel_cache_ttl_seconds: int = Field(default=900, alias="SENTINEL_CACHE_TTL_SECONDS")
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()

