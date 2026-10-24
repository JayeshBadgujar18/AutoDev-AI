from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AutoDev AI"
    environment: str = "development"
    database_url: str = "sqlite+aiosqlite:///./autodev.db"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "autodev_memory"
    max_debug_iterations: int = 5
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
