from pydantic import Field

from core.schemas.base import CamelBaseModel

from .extended_mixins import BasicLevelTemplate, BasicSkillsTemplate
from .pydantic_mixins import BasicUserDataMixin, DateTimeMixin, EmailMixin, IdMixin


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
    BasicUserDataMixin,
    EmailMixin,
    DateTimeMixin,
    IdMixin,
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
