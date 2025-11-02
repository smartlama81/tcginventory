from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = "TCG Inventory Backend"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    api_prefix: str = "/api/v1"
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TCGINV_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
