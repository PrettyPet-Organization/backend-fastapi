from datetime import datetime

from core.schemas.base import CamelBaseModel

from .pydantic_mixins import IdMixin


class ApplicationResponseTemplate(IdMixin, CamelBaseModel):
    project_role_id: int | None
    user_id: int | None
    application_status: str | None
    response_text: str | None
    reviewed_at: datetime | None
    reviewed_by_user_id: int | None


class TokenResponse(CamelBaseModel):
    access_token: str
    token_type: str


class ErrorResponse(CamelBaseModel):
    detail: str
