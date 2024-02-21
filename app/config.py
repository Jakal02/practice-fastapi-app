from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Settings for this API."""

    database_url: PostgresDsn
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )


settings = APISettings()
