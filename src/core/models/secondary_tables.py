from sqlalchemy import Column, DateTime, ForeignKey, Table, func

from .base import Base


project_role_skills = Table(
    "project_role_skills",
    Base.metadata,
    Column("role_id", ForeignKey("project_roles.id")),
    Column("skill_id", ForeignKey("skills.id")),
)

user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("skill_id", ForeignKey("skills.id")),
)

project_role_users = Table(
    "project_role_users",
    Base.metadata,
    Column("project_role_id", ForeignKey("project_roles.id")),
    Column("users_id", ForeignKey("users.id")),
    Column("created_at", DateTime, server_default=func.now()),
)
