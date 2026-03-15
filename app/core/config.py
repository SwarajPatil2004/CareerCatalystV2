from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import Optional, List

class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: Environment = Environment.DEV
    SENTRY_DSN: Optional[str] = None
    
    # Auth settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Redis for caching/rate-limiting
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Celery configuration
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # Security
    PII_ENCRYPTION_KEY: Optional[str] = None
    ALLOWED_HOSTS: List[str] = ["*"]

    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "100/hour"

    # CORS settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
