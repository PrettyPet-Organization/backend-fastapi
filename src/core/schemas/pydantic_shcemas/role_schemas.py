from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from .pydantic_mixins import (
    IdMixin,
    RoleEssentialsMixin,
    RoleTypeMixin,
    DateTimeMixin,
    BasicUserDataMixin,
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    EmailMixin
)
from .extended_mixins import (
    BasicRoleTemplate,
    BasicSkillsTemplate
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
