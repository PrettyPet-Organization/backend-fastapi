from core.schemas.base import CamelBaseModel

from .extended_mixins import BasicRoleTemplate
from .pydantic_mixins import (
    DecimalProjectMixin,
    IdMixin,
    ProjectEssentialsMixin,
    RoleEssentialsMixin,
)
from datetime import datetime

class ApplicationResponseTemplate(
    IdMixin,
    CamelBaseModel
):
    project_role_id: int | None
    user_id: int | None
    application_status: str | None
    response_text: str | None
    reviewed_at: datetime | None
    reviewed_by_user_id: int | None


