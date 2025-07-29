from pydantic import BaseModel
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
    BaseModel,
    BasicSkillsTemplate
):
    message: str = "Skill added successfully"


class UserOutputTemplate(
    BaseModel,
    BasicUserDataMixin,
    EmailMixin,
    DateTimeMixin,
    IdMixin
):
    
    level: BasicLevelTemplate | None
    skills: list[BasicSkillsTemplate] | None



class PutUserTemplate(
    BaseModel,
    BasicUserDataMixin,    
    EmailMixin
):
    pass