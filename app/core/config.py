"""Environment-backed settings. No credentials are stored in source."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ScholarBee AI Backend"
    # Convenient for local FlutterFlow/browser testing. Set a strict origin
    # list in deployment environments; credentials are disabled in main.py.
    cors_origins: list[str] = ["*"]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
