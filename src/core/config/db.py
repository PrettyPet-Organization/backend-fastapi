import pydantic_settings
import sqlalchemy


class DatabaseSettings(pydantic_settings.BaseSettings):
    url: str | sqlalchemy.URL
    echo: bool
