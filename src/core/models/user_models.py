from typing import Annotated

from fastapi import Depends
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, CreatedAtMixin, UpdatedAtMixin, get_str_field
from .secondary_tables import project_role_skills, project_role_users, user_skills


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
        secondary=project_role_skills, back_populates="skills"
    )


class ProjectRolesBase(Base):
    __tablename__ = "project_roles"

    role_type_id: Mapped[int] = mapped_column(ForeignKey("role_types.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    description: Mapped[str]
    required_skills_description: Mapped[str]
    number_of_needed: Mapped[int]

    skills: Mapped[list["SkillsBase"]] = relationship(
        secondary=project_role_skills, back_populates="project_roles"
    )
    role_types: Mapped["RoleTypesBase"] = relationship(back_populates="project_roles")
    project: Mapped["ProjectBase"] = relationship(back_populates="roles")
    users: Mapped[list["UsersBase"]] = relationship(
        secondary=project_role_users, back_populates="project_roles"
    )


class ProjectBase(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "projects"

    title: Mapped[Annotated[str, Depends(get_str_field)]]
    description: Mapped[str]
    desired_fundraising_amount: Mapped[int]
    entry_ticket_price: Mapped[int]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator: Mapped["UsersBase"] = relationship(back_populates="project")
    roles: Mapped[list["ProjectRolesBase"]] = relationship(back_populates="project")


class RoleTypesBase(Base):
    __tablename__ = "role_types"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    project_roles: Mapped[list["ProjectRolesBase"]] = relationship(
        back_populates="role_type"
    )


class UsersBase(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    email: Mapped[Annotated[str, Depends(get_str_field)]]
    password_hash: Mapped[Annotated[str, Depends(get_str_field)]]
    full_name: Mapped[Annotated[str, Depends(get_str_field)]]
    bio: Mapped[str]
    preferences: Mapped[str]
    experience: Mapped[str]
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))

    oauth_account: Mapped["OauthAccountsBase"] = relationship(back_populates="user")
    skills: Mapped[list["SkillsBase"]] = relationship(
        secondary=user_skills, back_populates="users"
    )
    level: Mapped["LevelsBase"] = relationship(back_populates="users")
    projects: Mapped[list["ProjectBase"]] = relationship(back_populates="creator")
    roles: Mapped[list["ProjectRolesBase"]] = relationship(
        secondary=project_role_users, back_populates="users"
    )


class LevelsBase(Base):
    __tablename__ = "levels"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    users: Mapped[list["UsersBase"]] = relationship(back_populates="level")
