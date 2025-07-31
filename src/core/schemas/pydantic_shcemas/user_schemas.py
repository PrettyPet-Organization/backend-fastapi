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
    BasicSkillsTemplate,
    BaseModel
):
    message: str = "Skill added successfully"


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