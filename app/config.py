from functools import lru_cache

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    app_name: str = "Multi-Agent AI API"
    app_version: str = "1.0.0"

    database_url: str = (
        "sqlite:///database/app.db"
    )

    secret_key: str = Field(
        default=(
            "CHANGE_ME_TO_A_LONG_"
            "RANDOM_SECRET_KEY"
        ),
        min_length=32,
    )

    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = Field(
        default=60,
        gt=0,
    )

    gemini_api_key: str | None = None

    model_name: str = "gemini-2.0-flash"

    serper_api_key: str | None = None

    # Keep environment parsing simple.
    # Example:
    # CORS_ORIGINS_RAW=http://localhost:5173,http://127.0.0.1:5173
    cors_origins_raw: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins_raw.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


# Compatibility constants.

GEMINI_API_KEY = settings.gemini_api_key
MODEL_NAME = settings.model_name
SERPER_API_KEY = settings.serper_api_key
CORS_ORIGINS = settings.cors_origins
MAX_MESSAGE_LENGTH = 10_000