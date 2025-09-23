from pydantic import Field

from core.schemas.base import CamelBaseModel

from .extended_mixins import BasicLevelTemplate, BasicSkillsTemplate
from .pydantic_mixins import BasicUserDataMixin, DateTimeMixin, EmailMixin, IdMixin


class UserOutputTrimmedTemplate(
    BasicUserDataMixin,
    EmailMixin,
    DateTimeMixin,
    IdMixin,
    CamelBaseModel
):
    pass

class SkillsWithMessageTemplate(
    BasicSkillsTemplate,
    CamelBaseModel
):
    message: str = "Skill added successfully"


class SkillsWithRoleIDTemplate(
    SkillsWithMessageTemplate
):
    id: int = Field(ge=1, alias="role_id")


class UserOutputTemplate(
    UserOutputTrimmedTemplate,
    CamelBaseModel
):

    level: BasicLevelTemplate | None
    skills: list[BasicSkillsTemplate] | None



class PutUserTemplate(
    BasicUserDataMixin,
    EmailMixin,
    CamelBaseModel
):
    pass
