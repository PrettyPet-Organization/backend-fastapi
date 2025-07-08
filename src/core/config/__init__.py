import os
from collections.abc import AsyncGenerator

import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from str2bool import str2bool_exc
from core.config.db import DatabaseSettings
from core.config.logging import LOGGING_CONFIG, logger
from core.config.main import BASE_DIR, Settings
from dotenv import load_dotenv


load_dotenv()

DOTENV_MODE = str2bool_exc(os.getenv("DOTENV_MODE", "false"))

pg_internal_host = "localhost" if DOTENV_MODE else os.environ["PG_INTERNAL_HOST"]

DEBUG = str2bool_exc(os.environ["DEBUG"])
PG_DATABASE_NAME = os.environ["PG_DATABASE_NAME"]
PG_USER_NAME = os.environ["PG_USER_NAME"]
PG_USER_PASSWORD = os.environ["PG_USER_PASSWORD"]
PG_INTERNAL_PORT = int(os.environ["PG_INTERNAL_PORT"])


db_url = sqlalchemy.URL.create(
    drivername="postgresql+psycopg",
    username=PG_USER_NAME,
    password=PG_USER_PASSWORD,
    host=pg_internal_host,
    port=PG_INTERNAL_PORT,
    database=PG_DATABASE_NAME,
)


db_settings = DatabaseSettings(url=db_url, echo=True)
settings = Settings(debug=DEBUG, db=db_settings)

async_db_engine = create_async_engine(settings.db.url, echo=settings.db.echo)
async_db_session_factory = async_sessionmaker(async_db_engine)

async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_db_session_factory() as session:
        yield session

__all__ = (
    "settings",
    "BASE_DIR",
    "async_db_engine",
    "async_db_session_factory",
    "logger",
    "LOGGING_CONFIG",
)
