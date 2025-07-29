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
    BaseModel,
    RoleEssentialsMixin,
    IdMixin
):
    role_types: BasicRoleTemplate | None
    project_id: int | None


class RoleInputTemplate(
    BaseModel,
    RoleEssentialsMixin
):
    pass


class UserTemplateProto(
    BaseModel,
    DateTimeMixin,
    BasicUserDataMixin,
    EmailMixin,
    IdMixin
):
    pass


class ProjectTemplate(
    BaseModel,
    ProjectEssentialsMixin,
    DecimalProjectMixin,
    IdMixin
):
    creator: UserTemplateProto


class RoleExtendedOutputTemplate(
    BaseModel,
    RoleEssentialsMixin,
    IdMixin
):
    role_types: BasicRoleTemplate | None
    project_id: int | None

    project: ProjectTemplate
