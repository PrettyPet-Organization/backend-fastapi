import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from core.models.base import Base
from main import app
from core.dependencies.auth import get_db

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/test_db"

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Override event loop for Windows compatibility."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def prepare_database(event_loop):
    async def _init_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    event_loop.run_until_complete(_init_db())
    yield
    event_loop.run_until_complete(test_engine.dispose())


@pytest.fixture()
def db_session():
    async def _get_session():
        async with TestingSessionLocal() as session:
            yield session

    session = asyncio.get_event_loop().run_until_complete(_get_session().__anext__())
    return session


@pytest.fixture()
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as client:
        yield client
