from pydantic import BaseModel

from .extended_mixins import BasicRoleTemplate
from .pydantic_mixins import (
    DecimalProjectMixin,
    IdMixin,
    ProjectEssentialsMixin,
    RoleEssentialsMixin,
)


class NewProjectTemplate(
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    BaseModel
):
    pass


class CreatorTemplate(
    IdMixin,
    BaseModel
):
    pass

class RoleTemplate(
    RoleEssentialsMixin,
    IdMixin,
    BaseModel
):
    role_types: BasicRoleTemplate


class ProjectTemplateV2(
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin,
    BaseModel
):
    creator_id: int | None
    roles: list[RoleTemplate] | None


class ProjectTemplateShort(
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin,
    BaseModel
):
    creator_id: int | None


