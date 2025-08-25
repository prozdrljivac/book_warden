from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional

DEVELOPMENT_ENVIRONMENT = Literal["DEV", "PROD"]
LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    app_secret_key: str
    db_url: str = "db/dev.db"
    server_port: str
    environment: DEVELOPMENT_ENVIRONMENT = "DEV"
    log_level: LOG_LEVEL = "INFO"
    log_path: Optional[str]

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
