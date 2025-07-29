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

# class RoleTemplate(
#     BaseModel,
#     RoleTypeMixin
# ):
#     pass


class NewProjectTemplate(
    BaseModel,
    DecimalProjectMixin,
    ProjectEssentialsMixin
):
    pass


class CreatorTemplate(
    BaseModel,
    IdMixin
):
    pass 
    
class RoleTemplate(
    BaseModel,
    RoleEssentialsMixin,
    IdMixin
):
    role_types: BasicRoleTemplate


class ProjectTemplateV2(
    BaseModel,
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin    
):
    creator_id: int | None
    roles: list[BasicRoleTemplate] | None


class ProjectTemplateShort(
    BaseModel,
    DecimalProjectMixin,
    ProjectEssentialsMixin,
    IdMixin
):
    creator_id: int | None


