import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URI: str
    ECHO_SQL: bool

    class Config:
        env = os.environ["APP_CONFIG_FILE"]
        env_file = Path(__file__).parent / f"config/{env}.env"
        case_sensitive = True
