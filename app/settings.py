import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"config/{os.environ['APP_CONFIG_FILE']}.env",
        case_sensitive=True,
    )


settings = Settings.model_validate({})
