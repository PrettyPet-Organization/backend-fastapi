import sqlalchemy
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    PG_USER_NAME: str
    PG_USER_PASSWORD: str
    PG_INTERNAL_HOST: str
    PG_EXTERNAL_PORT: int
    PG_DATABASE_NAME: str
    echo: bool = False
    url: sqlalchemy.engine.URL | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.url:
            self.url = sqlalchemy.engine.URL.create(
                drivername="postgresql+asyncpg",
                username=self.PG_USER_NAME,
                password=self.PG_USER_PASSWORD,
                host=self.PG_INTERNAL_HOST,
                port=self.PG_EXTERNAL_PORT,
                database=self.PG_DATABASE_NAME,
            )
