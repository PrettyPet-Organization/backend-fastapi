from pydantic import (
    BaseModel,
    Field
)
from datetime import datetime
from .pydantic_mixins import (
    IdMixin,
    EmailMixin,
    BasicUserDataMixin,
    DateTimeMixin
)
from .extended_mixins import (
    BasicLevelTemplate,
    BasicSkillsTemplate
)


class SkillsWithMessageTemplate(
    BasicSkillsTemplate,
    BaseModel
):
    message: str = "Skill added successfully"


class SkillsWithRoleIDTemplate(
    SkillsWithMessageTemplate
):
    id: int = Field(ge=1, alias="role_id")


class UserOutputTemplate(
    BasicUserDataMixin,
    EmailMixin,
    DateTimeMixin,
    IdMixin,
    BaseModel
):
    
    level: BasicLevelTemplate | None
    skills: list[BasicSkillsTemplate] | None



class PutUserTemplate(
    BasicUserDataMixin,    
    EmailMixin,
    BaseModel
):
    pass