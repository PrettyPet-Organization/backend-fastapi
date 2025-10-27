from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from ..models.user_models import User, UserProfile
from ..schemas import UserCreate
from ..auth.utils import hash_password
from .file_service import FileService


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.file_service = FileService()

    async def check_user_exists(self, email: str, username: str) -> None:
        existing_user = await self.db.execute(
            select(User).where((User.email == email) | (User.username == username))
        )
        existing_user = existing_user.scalar_one_or_none()

        if existing_user:
            if existing_user.email == email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this username already exists",
                )

    async def create_user(self, user_data: UserCreate) -> User:
        await self.check_user_exists(user_data.email, user_data.username)

        try:
            profile_photo_path = await self.file_service.save_base64_file(
                user_data.profile.profile_photo, "profile_photos"
            )

            resume_path = None
            if user_data.profile.resume:
                resume_path = await self.file_service.save_base64_file(
                    user_data.profile.resume, "resumes"
                )

            user = User(
                email=user_data.email,
                username=user_data.username,
                password_hash=hash_password(user_data.password),
                wallet_stars=3,  # Начальный бонус
            )
            self.db.add(user)
            await self.db.flush()

            profile = UserProfile(
                user_id=user.id,
                profile_photo=profile_photo_path,
                main_stack=user_data.profile.main_stack,
                resume=resume_path,
                hobbies=user_data.profile.hobbies,
                birth_date=user_data.profile.birth_date,
                city=user_data.profile.city,
            )
            self.db.add(profile)

            await self.db.commit()
            await self.db.refresh(user)
            await self.db.refresh(profile)

            return user

        except Exception as e:
            await self.db.rollback()
            if "profile_photo_path" in locals():
                await self.file_service.delete_file(profile_photo_path)
            if resume_path:
                await self.file_service.delete_file(resume_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}",
            )
