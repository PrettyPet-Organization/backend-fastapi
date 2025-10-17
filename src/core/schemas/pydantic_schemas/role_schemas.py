from core.schemas.base import CamelBaseModel

from .extended_mixins import BasicRoleTemplate
from .pydantic_mixins import (BasicUserDataMixin, DateTimeMixin,
                              DecimalProjectMixin, EmailMixin, IdMixin,
                              ProjectEssentialsMixin, RoleEssentialsMixin)


class RoleOutputTemplate(RoleEssentialsMixin, IdMixin, CamelBaseModel):
    role_types: BasicRoleTemplate | None
    project_id: int | None


class RoleInputTemplate(RoleEssentialsMixin, CamelBaseModel):
    pass


class UserTemplateProto(
    DateTimeMixin, BasicUserDataMixin, EmailMixin, IdMixin, CamelBaseModel
):
    pass


class ProjectTemplate(
    ProjectEssentialsMixin, DecimalProjectMixin, IdMixin, CamelBaseModel
):
    creator: UserTemplateProto


class RoleExtendedOutputTemplate(RoleEssentialsMixin, IdMixin, CamelBaseModel):
    role_types: BasicRoleTemplate | None
    project_id: int | None

    project: ProjectTemplate
