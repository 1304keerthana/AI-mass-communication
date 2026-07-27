from functools import lru_cache
from pathlib import Path

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    postgres_user: str = Field(...)
    postgres_password: str = Field(...)
    postgres_db: str = Field(...)
    postgres_host: str = Field("localhost")
    postgres_port: int = Field(5432)
    database_url: AnyUrl = Field(...)
    secret_key: str = Field(...)
    access_token_expire_minutes: int = Field(60)
    refresh_token_expire_minutes: int = Field(1440)

    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="forbid")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
