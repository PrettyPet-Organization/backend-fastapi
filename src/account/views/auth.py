from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import UserCreate, UserResponse, UserLogin, LoginResponse
from ..services.auth_service import AuthService
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate user and return JWT token"
)
async def login(
        form_data: UserLogin,
        db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    User login with email and password.

    Returns JWT access token that should be included in Authorization header
    for protected endpoints: `Authorization: Bearer {token}`
    """
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post(
    "/token",
    response_model=LoginResponse,
    include_in_schema=False
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)
) -> UserResponse:
    """Get current authenticated user."""
    return UserResponse.model_validate(current_user)


@router.post(
    "/refresh",
    response_model=LoginResponse,
    summary="Refresh access token",
    description="Refresh expired access token (требует реализации refresh токенов)"
)
async def refresh_token(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Refresh access token.
    В будущем можно добавить систему refresh токенов.
    """
    auth_service = AuthService(db)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": current_user.username},
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(current_user)
    )