from pydantic import Field

from core.schemas.base import CamelBaseModel

from .pydantic_mixins import IdMixin


class BasicLevelTemplate(IdMixin, CamelBaseModel):
    name: str = Field(min_length=4, max_length=255)


class BasicRoleTemplate(IdMixin, CamelBaseModel):
    name: str = Field(min_length=4, max_length=255)


class BasicSkillsTemplate(IdMixin, CamelBaseModel):
    name: str = Field(min_length=4, max_length=255)
