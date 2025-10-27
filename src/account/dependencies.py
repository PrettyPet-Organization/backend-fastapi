from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .services.auth_service import AuthService
from .models.user_models import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Зависимость для получения текущего пользователя."""
    auth_service = AuthService(db)
    return await auth_service.get_current_user(credentials.credentials)


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Зависимость для получения активного пользователя."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user