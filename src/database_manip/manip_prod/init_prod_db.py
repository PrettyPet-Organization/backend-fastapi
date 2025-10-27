from core.config.db import DatabaseSettings

db_config = DatabaseSettings()

DATABASE_URL = db_config.url

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sync_engine = create_engine(
    DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg")
)
sync_session = sessionmaker(bind=sync_engine)

sync_test_engine = create_engine(
    db_config.url_tests.replace("postgresql+asyncpg", "postgresql+psycopg")
)
