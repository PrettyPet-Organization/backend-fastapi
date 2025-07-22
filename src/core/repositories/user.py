from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user_models import UsersBase
from core.utils.security import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> UsersBase:
        hashed = hash_password(password)
        user = UsersBase(email=email, hashed_password=hashed)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> UsersBase | None:
        result = await self.session.execute(
            select(UsersBase).where(UsersBase.email == email)
        )
        return result.scalars().first()
