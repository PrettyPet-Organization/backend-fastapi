from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import Base, TimestampMixin
from src.account.utils.models_utils import get_str_field


class User(
    Base,
    TimestampMixin,
):
    __tablename__ = "users"

    email: Mapped[Annotated[str, Depends(get_str_field)]]
    username: Mapped[Annotated[str, Depends(get_str_field)]]
    password_hash: Mapped[str]
    wallet_stars: Mapped[int] = mapped_column(default=3)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    oauth_accounts: Mapped[list["OauthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    skills: Mapped[list["Skill"]] = relationship(
        secondary="user_skills", back_populates="users"
    )


class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"

    # required
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    profile_photo: Mapped[str | None] = mapped_column(nullable=False)
    main_stack: Mapped[List[str] | None] = mapped_column(JSONB, nullable=False)

    # not required
    resume: Mapped[str | None] = mapped_column(nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    hobbies: Mapped[List[str] | None] = mapped_column(JSONB, nullable=True)
    city: Mapped[str | None] = mapped_column(nullable=True)
    github: Mapped[str | None] = mapped_column(nullable=True)
    linkedin: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="profile")


class OauthAccount(Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[Annotated[str, Depends(get_str_field)]]
    provider_user_id: Mapped[Annotated[str, Depends(get_str_field)]]
    access_token: Mapped[str | None] = mapped_column(nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(nullable=True)
    expires_at: Mapped[int | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="oauth_accounts")


class Skill(Base):
    __tablename__ = "skills"

    name: Mapped[Annotated[str, Depends(get_str_field)]]
    category: Mapped[str | None] = mapped_column(nullable=True)

    users: Mapped[list["User"]] = relationship(
        secondary="user_skills", back_populates="skills"
    )


# Association tables
class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
