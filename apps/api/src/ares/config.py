from __future__ import annotations

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    MINIO_ENDPOINT: str = 'localhost:9000'
    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'
    MINIO_BUCKET: str = 'ares-documents'
    MINIO_USE_SSL: bool = False
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    CORS_ORIGINS: list[str] = ['http://localhost:3000']
    LOG_LEVEL: str = 'INFO'
    ENVIRONMENT: str = 'development'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore
