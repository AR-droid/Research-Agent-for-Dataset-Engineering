from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ares"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # MinIO / S3 Configuration
    MINIO_ENDPOINT: str = 'localhost:9000'
    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'
    MINIO_BUCKET: str = 'ares-documents'
    MINIO_USE_SSL: bool = False
    
    # Security
    JWT_SECRET_KEY: str = "development-secret-key-do-not-use-in-production"
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Environment
    CORS_ORIGINS: list[str] = ['http://localhost:3000']
    LOG_LEVEL: str = 'INFO'
    ENVIRONMENT: str = 'development'
    
    # External APIs
    GEMINI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore
