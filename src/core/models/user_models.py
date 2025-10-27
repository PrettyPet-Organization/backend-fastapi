from datetime import datetime, date
from decimal import Decimal
from typing import Annotated, List

from fastapi import Depends
from sqlalchemy import ForeignKey, Numeric, String, Date
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import (
    Base,
    CreatedAtMixin,
    UpdatedAtMixin,
    get_str_field,
    get_str_field_nullable,
)


class OauthAccountsBase(Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    provider: Mapped[Annotated[str, Depends(get_str_field)]]
    provider_user_id: Mapped[Annotated[str, Depends(get_str_field)]]

    user: Mapped["UsersBase"] = relationship(back_populates="oauth_account")


class SkillsBase(Base):
    __tablename__ = "skills"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    users: Mapped[list["UsersBase"]] = relationship(
        secondary="user_skills", back_populates="skills"
    )
    roles: Mapped[list["ProjectRolesBase"]] = relationship(
        secondary="project_role_skills", back_populates="skills"
    )


class ProjectRolesBase(Base):
    __tablename__ = "project_roles"

    role_type_id: Mapped[int] = mapped_column(ForeignKey("role_types.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    description: Mapped[str]
    required_skills_description: Mapped[str]
    number_of_needed: Mapped[int]

    skills: Mapped[list["SkillsBase"]] = relationship(
        secondary="project_role_skills", back_populates="roles"
    )
    role_types: Mapped["RoleTypesBase"] = relationship(back_populates="project_roles")
    project: Mapped["ProjectBase"] = relationship(back_populates="roles")
    users: Mapped[list["UsersBase"]] = relationship(
        secondary="project_role_users", back_populates="roles"
    )
    project_role_response: Mapped[list["ProjectRoleResponseBase"]] = relationship(
        back_populates="project_role"
    )


class ProjectBase(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "projects"

    title: Mapped[Annotated[str, Depends(get_str_field)]]
    description: Mapped[str]
    desired_fundraising_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    entry_ticket_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[Annotated[str, Depends(get_str_field)]] = mapped_column(
        server_default="pending"
    )
    approved_by_admin_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(nullable=True)
    rejection_reason_id: Mapped[int | None] = mapped_column(
        ForeignKey("rejection_reason.id"), nullable=True
    )

    creator: Mapped["UsersBase"] = relationship(
        foreign_keys=[creator_id], back_populates="projects"
    )
    roles: Mapped[list["ProjectRolesBase"]] = relationship(back_populates="project")
    rejection_reason: Mapped["RejectionReasonBase"] = relationship(
        back_populates="projects"
    )
    approved_by: Mapped["UsersBase"] = relationship(
        back_populates="projects_approved", foreign_keys=[approved_by_admin_id]
    )


class RejectionReasonBase(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "rejection_reason"

    reason_text: Mapped[Annotated[str, Depends(get_str_field)]]
    description: Mapped[str | None]

    projects: Mapped[list["ProjectBase"]] = relationship(
        back_populates="rejection_reason"
    )


class RoleTypesBase(Base):
    __tablename__ = "role_types"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    project_roles: Mapped[list["ProjectRolesBase"]] = relationship(
        back_populates="role_types"
    )


class ProjectRoleResponseBase(Base, CreatedAtMixin):
    __tablename__ = "project_role_response"

    project_role_id: Mapped[int] = mapped_column(ForeignKey("project_roles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    application_status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    response_text: Mapped[str | None] = mapped_column(nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    reviewed_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    project_role: Mapped["ProjectRolesBase"] = relationship(
        back_populates="project_role_response"
    )
    respondee: Mapped["UsersBase"] = relationship(
        back_populates="application_responses", foreign_keys=[user_id]
    )
    approved_by: Mapped["UsersBase"] = relationship(
        back_populates="applications_approved", foreign_keys=[reviewed_by_user_id]
    )


class UsersBase(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    email: Mapped[Annotated[str, Depends(get_str_field)]]
    username: Mapped[Annotated[str, Depends(get_str_field)]]  # новое поле
    password_hash: Mapped[str]
    full_name: Mapped[Annotated[str | None, Depends(get_str_field_nullable)]]
    profile_photo: Mapped[str | None] = mapped_column(nullable=True)  # путь к файлу
    resume: Mapped[str | None] = mapped_column(nullable=True)  # путь к файлу резюме
    bio: Mapped[str | None] = mapped_column(nullable=True)
    hobbies: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=True
    )  # PostgreSQL
    main_stack: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=True
    )  # PostgreSQL
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    city: Mapped[str | None] = mapped_column(nullable=True)
    wallet_stars: Mapped[int] = mapped_column(default=3)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)
    oauth_account: Mapped["OauthAccountsBase"] = relationship(back_populates="user")
    skills: Mapped[list["SkillsBase"]] = relationship(
        secondary="user_skills", back_populates="users"
    )
    level: Mapped["LevelsBase"] = relationship(back_populates="users")
    projects: Mapped[list["ProjectBase"]] = relationship(
        back_populates="creator", foreign_keys=[ProjectBase.creator_id]
    )
    roles: Mapped[list["ProjectRolesBase"]] = relationship(
        secondary="project_role_users", back_populates="users"
    )
    user_role: Mapped[list["RolesBase"]] = relationship(
        back_populates="user", secondary="user_roles"
    )
    projects_approved: Mapped[list["ProjectBase"]] = relationship(
        back_populates="approved_by", foreign_keys=[ProjectBase.approved_by_admin_id]
    )
    applications_approved: Mapped[list["ProjectRoleResponseBase"]] = relationship(
        back_populates="approved_by",
        foreign_keys=[ProjectRoleResponseBase.reviewed_by_user_id],
    )
    application_responses: Mapped[list["ProjectRoleResponseBase"]] = relationship(
        back_populates="respondee", foreign_keys=[ProjectRoleResponseBase.user_id]
    )


class LevelsBase(Base):
    __tablename__ = "levels"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    users: Mapped[list["UsersBase"]] = relationship(back_populates="level")


class ProjectRoleSkillsAssociation(Base):
    __tablename__ = "project_role_skills"

    role_id: Mapped[int] = mapped_column(ForeignKey("project_roles.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))


class UserSkillsAssociation(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))


class ProjectRoleUsersAssociation(Base, CreatedAtMixin):
    __tablename__ = "project_role_users"

    project_role_id: Mapped[int] = mapped_column(ForeignKey("project_roles.id"))
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class UserRolesAssociation(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), server_default="1")


class RolesBase(Base):
    __tablename__ = "roles"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    user: Mapped[list[UsersBase]] = relationship(
        back_populates="user_role", secondary="user_roles"
    )
