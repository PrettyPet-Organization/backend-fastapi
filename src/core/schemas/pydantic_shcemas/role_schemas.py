from pydantic import BaseModel

from .extended_mixins import BasicRoleTemplate
from .pydantic_mixins import (
    BasicUserDataMixin,
    DateTimeMixin,
    DecimalProjectMixin,
    EmailMixin,
    IdMixin,
    ProjectEssentialsMixin,
    RoleEssentialsMixin,
)


class RoleOutputTemplate(
    RoleEssentialsMixin,
    IdMixin,
    BaseModel
):
    role_types: BasicRoleTemplate | None
    project_id: int | None


class RoleInputTemplate(
    RoleEssentialsMixin,
    BaseModel
):
    pass


class UserTemplateProto(
    DateTimeMixin,
    BasicUserDataMixin,
    EmailMixin,
    IdMixin,
    BaseModel
):
    pass


class ProjectTemplate(
    ProjectEssentialsMixin,
    DecimalProjectMixin,
    IdMixin,
    BaseModel
):
    creator: UserTemplateProto


class RoleExtendedOutputTemplate(
    RoleEssentialsMixin,
    IdMixin,
    BaseModel
):
    role_types: BasicRoleTemplate | None
    project_id: int | None

    project: ProjectTemplate
