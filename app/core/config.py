from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ENVIRONMENT: Environment = Environment.DEV

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
