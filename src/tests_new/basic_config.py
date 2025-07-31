from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)
from collections.abc import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config.db import DatabaseSettings
from fastapi.testclient import TestClient
from sqlalchemy.pool import NullPool
from core.config import get_db
from core.models.base import Base
from main import app
import pytest



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
