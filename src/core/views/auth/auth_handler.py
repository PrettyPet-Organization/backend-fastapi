from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from core.config import get_db
from core.dependencies.auth import get_current_user
from core.models.user_models import UsersBase, UserRolesAssociation
from core.schemas.user import UserCreate, UserLogin, UserRead
from core.utils.jwt import create_access_token
from core.utils.security import hash_password, verify_password
from core.schemas.pydantic_shcemas.user_schemas import UserOutputTemplate


auth_router = APIRouter()
bearer_scheme = HTTPBearer()


@auth_router.post("/register", response_model=UserOutputTemplate, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UsersBase:
    """Registration of a new user."""
    user_exists = await db.scalar(select(exists().where(UsersBase.email == user_create.email)))
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    new_user = UsersBase(
        email=user_create.email,
        password_hash=hash_password(user_create.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    new_user_role = UserRolesAssociation(
        user_id = new_user.id
    )
    
    db.add(new_user_role)
    await db.commit()

    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JSONResponse:
    """User authentication and issuing of a JWT token."""
    result = await db.execute(select(UsersBase).where(UsersBase.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user.id)})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"accessToken": token, "tokenType": "bearer"},
    )


@auth_router.get("/me", dependencies=[Security(bearer_scheme)], response_model=UserRead)
async def read_current_user(
    current_user: Annotated[UsersBase, Depends(get_current_user)]
) -> UsersBase:
    """Retrieve information about the current user."""
    return current_user
