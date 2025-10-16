from pydantic import Field

from core.schemas.base import CamelBaseModel


class PaginationTemplate(CamelBaseModel):
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
