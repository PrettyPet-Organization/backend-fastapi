from pydantic import (
    BaseModel,
    Field
)
from datetime import datetime
from decimal import Decimal
from .user_patterns import (
    IdMixin,
    UserCompleteDataTemplate,
    SkillsVitalTemplate,
    CreatorDataMixin
)
from .role_patterns import (
    CompleteRoleTemplate
)

class TimeMixin(
    BaseModel
):
    created_at: datetime
    updated_at: datetime    

class ProjectImputableTemplate(
    IdMixin,
    BaseModel
):
    title: str
    description: str
    desired_fundraising_amount: Decimal
    entry_ticket_price: Decimal


class ProjectTemplate(
    ProjectImputableTemplate,
    TimeMixin,
    BaseModel
):
    creator_id: int

class RoleTemplateExtended(
    CompleteRoleTemplate,
    BaseModel
):
    users: list[UserCompleteDataTemplate]
    skills: list[SkillsVitalTemplate]


class ExtendedProjectTemplate(
    ProjectImputableTemplate,
    TimeMixin,
    BaseModel
):
    creator: CreatorDataMixin
    roles: list[RoleTemplateExtended]



class RoleInputTemplate(
    BaseModel
):
    id: int


class FullProjectTemplate(
    ExtendedProjectTemplate,
    BaseModel
):
    pass