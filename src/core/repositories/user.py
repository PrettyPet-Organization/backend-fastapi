from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user import User
from core.utils.security import hash_password
from sqlalchemy import select

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> User:
        hashed = hash_password(password)
        user = User(email=email, hashed_password=hashed)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
