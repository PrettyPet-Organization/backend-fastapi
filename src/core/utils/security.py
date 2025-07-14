from passlib.context import CryptContext
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies.auth import get_db, get_current_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




def is_allowed(
    user_id: int,
    password: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> bool:
    pass