from core.schemas.base import CamelBaseModel

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
    CamelBaseModel
):
    pass


class CreatorTemplate(
    IdMixin,
    CamelBaseModel
):
    pass

class RoleTemplate(
    RoleEssentialsMixin,
    IdMixin,
    CamelBaseModel
):
    role_types: BasicRoleTemplate


class ProjectTemplateShort(
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin,
    CamelBaseModel
):
    creator_id: int | None


class ProjectTemplateWithRoles(
    ProjectTemplateShort,
    CamelBaseModel
):
    roles: list[RoleTemplate] | None




