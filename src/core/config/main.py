from pathlib import Path

import pydantic_settings

from core.config.db import DatabaseSettings

BASE_DIR = Path(__file__).parent.parent.parent  # ./src/


class Settings(pydantic_settings.BaseSettings):
    debug: bool
    db: DatabaseSettings
