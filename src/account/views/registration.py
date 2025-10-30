from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.db import get_db
from account.schemas.base import UserCreate, UserResponse
from account.services.user_service import UserService

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="📝 Register New User",
    description="""
    Register a new user in the PrettyPet platform.

    This endpoint creates a complete user profile with:
    - User account credentials
    - Personal profile information  
    - Initial wallet with 3 stars
    - Skill associations

    **Required fields:**
    - Email (must be unique)
    - Username (3-50 chars, letters/numbers/underscores only)
    - Password (min 8 chars with letters and digits)
    - Profile photo (URL or base64)
    - Main tech stack (at least one technology)

    **Optional fields:**
    - Resume file
    - Hobbies list
    - Birth date (must be 13+ years old)
    - City
    """,
    responses={
        201: {
            "description": "✅ User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "john_doe",
                        "wallet_stars": 3,
                        "is_active": True,
                        "profile": {
                            "profile_photo": "https://example.com/photo.jpg",
                            "main_stack": ["Python", "FastAPI"],
                        },
                    }
                }
            },
        },
        400: {
            "description": "❌ Validation error",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists"}
                }
            },
        },
        500: {
            "description": "🔴 Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Registration failed: database error"}
                }
            },
        },
    },
)
async def register_user(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user account with complete profile setup.

    Each new user receives 3 stars in their wallet as a welcome bonus.
    The system automatically creates associated profile records.
    """
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        return UserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )
