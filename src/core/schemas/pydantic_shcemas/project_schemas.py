from pydantic import BaseModel
from decimal import Decimal
from .pydantic_mixins import (
    RoleTypeMixin,
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    BasicUserDataMixin,
    RoleEssentialsMixin,
    IdMixin
)
from .extended_mixins import (
    BasicRoleTemplate
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
    roles: list[BasicRoleTemplate] | None


class ProjectTemplateShort(
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin,
    BaseModel
):
    creator_id: int | None


