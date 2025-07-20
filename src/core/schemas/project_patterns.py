from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from .user_patterns import (
    UserDataPublicTemplate,
    SkillsVitalTemplate
)

class TimeMixin(BaseModel):
    created_at: datetime
    updated_at: datetime    

class ProjectImputableTemplate(BaseModel):
    title: str
    description: str
    desired_fundraising_amount: Decimal
    entry_ticket_price: Decimal


class ProjectTemplate(
    ProjectImputableTemplate,
    BaseModel
):
    id: int
    created_at: datetime
    updated_at: datetime
    creator_id: int


class ExtendedProjectTemplate(
    ProjectImputableTemplate,
    TimeMixin,
    BaseModel
):
    roles: list[SkillsVitalTemplate]
    assigned_user: list[UserDataPublicTemplate]



class RoleInputTemplate(
    BaseModel
):
    id: int