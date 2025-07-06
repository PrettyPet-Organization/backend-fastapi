import sqlalchemy
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


load_dotenv()

class DatabaseSettings(BaseSettings):
    url: str | sqlalchemy.URL
    echo: bool = False

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


db_settings = DatabaseSettings()

engine = create_async_engine(str(db_settings.url), echo=db_settings.echo)
async_session = async_sessionmaker(engine, expire_on_commit=False)
