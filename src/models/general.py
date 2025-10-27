from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models._base import UUIDPK, Base, CreatedAt, IntPK, UniqueStr, UpdatedAt
from src.models.types_ import SkillLevel


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUIDPK] = mapped_column("user_id")

    email: Mapped[UniqueStr]
    password_hash: Mapped[str]
    name: Mapped[str]
    bio: Mapped[str]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    oauth_accounts: Mapped[set[OAuthAccount]] = relationship(back_populates="user")
    skills: Mapped[set[Skill]] = relationship(
        secondary="users_skills", back_populates="users"
    )
    projects: Mapped[set[Project]] = relationship(
        secondary="projects_participants", back_populates="participants"
    )


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    id: Mapped[IntPK] = mapped_column("oauth_account_id")

    provider_user_id: Mapped[str]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    provider_id: Mapped[int] = mapped_column(
        ForeignKey("oauth_providers.oauth_provider_id", ondelete="CASCADE")
    )

    user: Mapped[User] = relationship(back_populates="oauth_accounts")
    provider: Mapped[OAuthProvider] = relationship(back_populates="oauth_accounts")


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id: Mapped[IntPK] = mapped_column("oauth_provider_id")

    name: Mapped[UniqueStr]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    oauth_accounts: Mapped[set[OAuthAccount]] = relationship(back_populates="provider")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[IntPK] = mapped_column("skill_id")

    name: Mapped[UniqueStr]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    users: Mapped[set[User]] = relationship(
        secondary="users_skills", back_populates="skills"
    )


class UserSkill(Base):
    __tablename__ = "users_skills"

    level: Mapped[SkillLevel]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    user_id: Mapped[UUIDPK] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    skill_id: Mapped[IntPK] = mapped_column(
        ForeignKey("skills.skill_id", ondelete="CASCADE")
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[IntPK] = mapped_column("project_id")

    title: Mapped[str]
    description: Mapped[str]
    desired_fundraising_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    entry_ticket_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    participants: Mapped[set[User]] = relationship(
        secondary="projects_participants", back_populates="projects"
    )
    needed_roles: Mapped[set[Role]] = relationship(secondary="projects_roles_needed")


class ProjectParticipant(Base):
    __tablename__ = "projects_participants"

    role_id: Mapped[int | None] = mapped_column(
        ForeignKey("roles.role_id", ondelete="SET NULL")
    )
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    project_id: Mapped[IntPK] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE")
    )
    participant_id: Mapped[UUIDPK] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[IntPK] = mapped_column("role_id")

    name: Mapped[UniqueStr]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    projects_needed: Mapped[set[Project]] = relationship(
        secondary="projects_roles_needed", back_populates="needed_roles"
    )


class ProjectRoleNeeded(Base):
    __tablename__ = "projects_roles_needed"

    needed_slots_count: Mapped[int]
    available_slots_count: Mapped[int]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    project_id: Mapped[IntPK] = mapped_column(
        ForeignKey("projects.project_id", ondelete="CASCADE")
    )
    role_id: Mapped[IntPK] = mapped_column(
        ForeignKey("roles.role_id", ondelete="CASCADE")
    )

    needed_skills: Mapped[set[ProjectRoleSkillNeeded]] = relationship(
        back_populates="project_role_needed"
    )


class ProjectRoleSkillNeeded(Base):
    __tablename__ = "projects_roles_skills_needed"
    __table_args__ = (
        ForeignKeyConstraint(
            ("project_id", "role_id"),
            ("projects_roles_needed.project_id", "projects_roles_needed.role_id"),
            ondelete="CASCADE",
        ),
    )

    min_level: Mapped[SkillLevel]
    created_at: Mapped[CreatedAt]
    updated_at: Mapped[UpdatedAt]

    project_id: Mapped[IntPK]
    role_id: Mapped[IntPK]
    skill_id: Mapped[IntPK] = mapped_column(ForeignKey("skills.skill_id"))

    project_role_needed: Mapped[ProjectRoleNeeded] = relationship(
        back_populates="needed_skills"
    )
    skill: Mapped[Skill] = relationship()
