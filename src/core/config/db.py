from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings
import sqlalchemy


class DatabaseSettings(BaseSettings):
    url: str | sqlalchemy.URL
    echo: bool = False

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


db_settings = DatabaseSettings()

engine = create_async_engine(str(db_settings.url), echo=db_settings.echo)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
