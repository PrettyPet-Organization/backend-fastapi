import os
from collections.abc import AsyncGenerator

import sqlalchemy
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from str2bool import str2bool_exc

load_dotenv()

DOTENV_MODE = str2bool_exc(os.getenv("DOTENV_MODE", "false"))
pg_internal_host = "localhost" if DOTENV_MODE else os.environ["PG_INTERNAL_HOST"]
DEBUG = str2bool_exc(os.environ["DEBUG"])
PG_DATABASE_NAME = os.environ["PG_DATABASE_NAME"]
PG_USER_NAME = os.environ["PG_USER_NAME"]
PG_USER_PASSWORD = os.environ["PG_USER_PASSWORD"]
PG_INTERNAL_PORT = int(os.environ["PG_INTERNAL_PORT"])


class DatabaseSettings(BaseSettings):
    PG_USER_NAME: str
    PG_USER_PASSWORD: str
    PG_INTERNAL_HOST: str
    PG_EXTERNAL_PORT: int
    PG_DATABASE_NAME: str
    PG_DATABASE_TESTS_NAME: str
    echo: bool = False
    url: sqlalchemy.engine.URL | None = None
    url_tests: sqlalchemy.engine.URL | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def __init__(self, **values):
        super().__init__(**values)
        if not self.url:
            self.url = self.__new_url_with_custom_name(self.PG_DATABASE_NAME)
        if not self.url_tests:
            self.url_tests = self.__new_url_with_custom_name(
                self.PG_DATABASE_TESTS_NAME
            )

    def __new_url_with_custom_name(self, db_name):
        url = sqlalchemy.engine.URL.create(
            drivername="postgresql+psycopg",
            username=self.PG_USER_NAME,
            password=self.PG_USER_PASSWORD,
            host=self.PG_INTERNAL_HOST,
            port=self.PG_EXTERNAL_PORT,
            database=db_name,
        )

        return url


db_settings = DatabaseSettings()

engine = create_async_engine(str(db_settings.url), echo=db_settings.echo)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
