from fastapi import APIRouter, HTTPException, status, Depends, Body, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.schemas.user import UserRead, UserCreate
from core.models.user import User
from core.config.db import get_db
from core.utils.security import hash_password, verify_password
from core.utils.jwt import create_access_token
from core.dependencies.auth import get_current_user
from fastapi.security import HTTPBearer
from core.schemas.user import UserLogin

router = APIRouter()

bearer_scheme = HTTPBearer()

@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_create.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    new_user = User(
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", dependencies=[Security(bearer_scheme)], response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
