from pydantic import (
    BaseModel,
    Field
)
from datetime import datetime
from decimal import Decimal
from .user_patterns import (
    UserCompleteDataTemplate,
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
    users: list[UserCompleteDataTemplate]



class RoleInputTemplate(
    BaseModel
):
    id: int


class FullProjectTemplate(
    ExtendedProjectTemplate,
    BaseModel
):
    pass