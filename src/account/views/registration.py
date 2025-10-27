from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import UserCreate, UserResponse
from ..services.user_service import UserService

router = APIRouter(prefix="/register", tags=["registration"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="""
    Register a new user with profile.

    Required fields:
    - email: valid email address
    - username: 3-50 characters, letters, numbers, underscores only
    - password: at least 8 characters with digit, letter and special character
    - profile_photo: base64 string or URL
    - main_stack: list of main technologies

    Optional fields:
    - resume: base64 string or URL
    - hobbies: list of hobbies
    - birth_date: date of birth (must be at least 13 years old)
    - city: city of residence
    """
)
async def register(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Register a new user account.

    Creates a new user with profile and initial wallet with 3 stars.
    """
    user_service = UserService(db)
    user = await user_service.create_user(user_data)
    return UserResponse.model_validate(user)