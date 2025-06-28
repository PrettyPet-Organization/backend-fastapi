from .base import (
    Base,
    CreatedAtMixin,
    UpdatedAtMixin,
    get_str_field
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    relationship,
    MappedColumn,
    mapped_column
)
from sqlalchemy import (
    ForeignKey,
    Table,
    Column
)
from fastapi import Depends
from typing import (
    Annotated,
    List
)
from .secondary_tables import project_role_skills



class OauthAccountsBase(Base):
    __tablename__ = "oauth_accounts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique = True)
    provider: Mapped[Annotated[str, Depends(get_str_field)]]
    provider_user_id: Mapped[Annotated[str, Depends(get_str_field)]]

    user: Mapped["UsersBase"] =  relationship(back_populates = "oauth_account")



class UserSkillsBase(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))    

    user: Mapped["UsersBase"] = relationship(back_populates = "user_skills")
    skills: Mapped["SkillsBase"] = relationship(back_populates = "skill")


class SkillsBase(Base):
    __tablename__ = "skills"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    users: Mapped[List["UserSkillsBase"]] = relationship("skill")
    project_roles: Mapped[List["ProjectRolesBase"]] = relationship("skills")


class ProjectRolesBase(Base):
    __tablename__ = "project_roles"

    role_type_id: Mapped[int] = mapped_column(ForeignKey("role_types.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    description: Mapped[str]
    required_skills_description: Mapped[str]
    number_of_needed: Mapped[int]

    skills: Mapped[List["SkillsBase"]] = relationship(secondary = project_role_skills)
    role_types: Mapped["RoleTypesBase"] = relationship(back_populates = "project_roles")
    project: Mapped["ProjectBase"] = relationship(back_populates = "roles")
    project_users_roles: Mapped[List["ProjectRoleUsersBase"]] = relationship(back_populates = "project_role") 


class ProjectBase(
    Base,
    CreatedAtMixin,
    UpdatedAtMixin
):
    __tablename__ = "projects"

    title: Mapped[Annotated[str, Depends(get_str_field)]]
    description: Mapped[str]
    desired_fundraising_amount: Mapped[int]
    entry_ticket_price: Mapped[int]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator: Mapped["UsersBase"] = relationship(back_populates = "project")
    roles: Mapped[List["ProjectRolesBase"]] = relationship(back_populates = "project")



class RoleTypesBase(Base):
    __tablename__ = "role_types"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    project_roles: Mapped[List["ProjectRolesBase"]] = relationship(back_populates = "role_type")


class UsersBase(
    Base,
    CreatedAtMixin,
    UpdatedAtMixin
):
    __tablename__ = "users"

    email: Mapped[Annotated[str, Depends(get_str_field)]]
    password_hash: Mapped[Annotated[str, Depends(get_str_field)]]
    full_name: Mapped[Annotated[str, Depends(get_str_field)]]
    bio: Mapped[str]
    preferences: Mapped[str]
    experience: Mapped[str]
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))

    level: Mapped["LevelsBase"] = relationship(back_populates = "users")
    oauth_account: Mapped["OauthAccountsBase"] = relationship(back_populates = "user")
    skills: Mapped[List["UserSkillsBase"]] = relationship(back_populates = "user")
    projects: Mapped[List["ProjectBase"]] = relationship(back_populates = "creator")
    project_roles: Mapped[List["ProjectRolesBase"]] = relationship(back_populates = "user")


class LevelsBase(Base):
    __tablename__ = "levels"

    name: Mapped[Annotated[str, Depends(get_str_field)]]

    users: Mapped[List["UsersBase"]] = relationship(back_populates = "level")


class ProjectRoleUsersBase(
    Base,
    CreatedAtMixin
):
    __tablename__ = "project_role_users"

    project_role_id: Mapped[int] = mapped_column(ForeignKey("project_roles.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    project_roles: Mapped["ProjectRolesBase"] = relationship(back_populates = "project_role_user")
    user: Mapped["UsersBase"] = relationship(back_populates = "project_role_user")

