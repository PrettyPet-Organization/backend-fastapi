from core.schemas.base import CamelBaseModel
from core.schemas.pydantic_schemas.extended_mixins import BasicRoleTemplate
from core.schemas.pydantic_schemas.pydantic_mixins import (  # RolesWithResponsesMixin,
    DecimalProjectMixin, IdMixin, ProjectEssentialsMixin, RoleEssentialsMixin)

from .response_schemas import ApplicationResponseTemplate


class BasicProjectTemplate(DecimalProjectMixin, ProjectEssentialsMixin, CamelBaseModel):
    pass


class CreatorTemplate(IdMixin, CamelBaseModel):
    pass


class RoleTemplate(RoleEssentialsMixin, IdMixin, CamelBaseModel):
    role_types: BasicRoleTemplate


class ProjectTemplateShort(
    DecimalProjectMixin, ProjectEssentialsMixin, IdMixin, CamelBaseModel
):
    creator_id: int | None


class ProjectTemplateWithRoles(ProjectTemplateShort, CamelBaseModel):
    roles: list[RoleTemplate] | None


class RolesWithResponsesMixin(IdMixin, RoleEssentialsMixin, CamelBaseModel):
    role_type_id: int | None
    project_id: int | None

    project_role_response: list[ApplicationResponseTemplate] | None


class ProjectRolesResponsesTemplate(ProjectTemplateShort, CamelBaseModel):
    roles: list[RolesWithResponsesMixin] | None
