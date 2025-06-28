from sqlalchemy import (
    Table,
    ForeignKey,
    Column
)
from .base import Base



project_role_skills = Table(
    "project_role_skills",
    Base.metadata,
    Column("role_id", ForeignKey("project_roles.id")),
    Column("skill_id", ForeignKey("skills.id"))
)