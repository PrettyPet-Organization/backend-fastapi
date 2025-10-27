from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column
from passlib.context import CryptContext


def get_str_field(
    length: int | None = 256, collation: str | None = None
) -> MappedColumn[String]:
    """Generate SQLAlchemy `mapped_column` for string fields."""
    return mapped_column(String(length=length, collation=collation))


def get_str_field_nullable(length: int | None = 256, collation: str | None = None):
    return mapped_column(String(length=length, collation=collation, nullable=True))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
