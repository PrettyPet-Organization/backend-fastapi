from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from core.config.db import DatabaseSettings

db_config = DatabaseSettings()
DATABASE_URL = db_config.url_tests.render_as_string(hide_password=False)

sync_test_engine = create_engine(DATABASE_URL, poolclass=NullPool)
sync_session = sessionmaker(sync_test_engine)


async_test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_test_session = async_sessionmaker(async_test_engine, expire_on_commit=False)
