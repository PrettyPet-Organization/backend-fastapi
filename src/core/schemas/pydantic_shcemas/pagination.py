from core.schemas.base import CamelBaseModel
from pydantic import Field


class PaginationTemplate(CamelBaseModel):
    page: int = Field(ge = 1)
    size: int = Field(ge = 1, le = 100)