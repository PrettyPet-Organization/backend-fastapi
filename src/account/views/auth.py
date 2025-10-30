from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.config.db import get_db
from account.schemas.base import UserLogin, LoginResponse
from account.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="🔐 User Login",
    description="""
    Authenticate user and generate JWT access token.

    After successful login, use the returned token in the Authorization header:
    `Authorization: Bearer <your_token>`

    The token is valid for 30 minutes by default.
    """,
    responses={
        200: {
            "description": "✅ Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIs...",
                        "token_type": "bearer",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "username": "john_doe",
                            "wallet_stars": 3,
                        },
                    }
                }
            },
        },
        401: {
            "description": "❌ Authentication failed",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        },
    },
)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Authenticate user credentials and return JWT token.

    - **email**: Registered email address
    - **password**: User password

    Returns access token for authorized API requests.
    Include this token in the Authorization header for protected endpoints.
    """
    auth_service = AuthService(db)

    user = await auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(access_token=access_token, token_type="bearer", user=user)


@router.post(
    "/refresh",
    summary="🔄 Refresh Token",
    description="Refresh expired access token (implementation pending)",
    responses={
        200: {
            "description": "✅ Token refresh endpoint",
            "content": {
                "application/json": {
                    "example": {"message": "Token refresh endpoint - to be implemented"}
                }
            },
        }
    },
)
async def refresh_token():
    """
    Refresh JWT access token.

    *This endpoint is planned for future implementation*
    Will allow refreshing expired tokens without re-authentication.
    """
    return {"message": "Token refresh endpoint - to be implemented"}
