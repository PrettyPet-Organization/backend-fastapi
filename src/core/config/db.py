from collections.abc import AsyncGenerator

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


class DatabaseSettings(BaseSettings):
    PG_USER_NAME: str
    PG_USER_PASSWORD: str
    PG_INTERNAL_HOST: str
    PG_INTERNAL_PORT: int
    PG_DATABASE_NAME: str
    PG_DATABASE_TESTS_NAME: str
    echo: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def url(self):
        """URL для asyncpg драйвера"""
        return f"postgresql+asyncpg://{self.PG_USER_NAME}:{self.PG_USER_PASSWORD}@{self.PG_INTERNAL_HOST}:{self.PG_INTERNAL_PORT}/{self.PG_DATABASE_NAME}"

    @property
    def url_tests(self):
        """URL для тестовой БД"""
        return f"postgresql+asyncpg://{self.PG_USER_NAME}:{self.PG_USER_PASSWORD}@{self.PG_INTERNAL_HOST}:{self.PG_INTERNAL_PORT}/{self.PG_DATABASE_TESTS_NAME}"


# Инициализация
db_settings = DatabaseSettings()

# Создаем engine с asyncpg
engine = create_async_engine(
    db_settings.url,
    echo=db_settings.echo,
    pool_pre_ping=True,  # проверка соединения перед использованием
    pool_recycle=3600,  # пересоздание соединений каждый час
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
