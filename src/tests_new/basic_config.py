from collections.abc import AsyncGenerator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from core.config import get_db
from core.config.db import DatabaseSettings
from main import app


db_config = DatabaseSettings()
DATABASE_URL = db_config.url_tests.render_as_string(hide_password=False)

sync_test_engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool
)
async_test_engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool
)
async_test_session = async_sessionmaker(
    async_test_engine,
    expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession]:
    async with async_test_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app=app)
