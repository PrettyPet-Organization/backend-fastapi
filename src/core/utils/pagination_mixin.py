from fastapi import Query

from core.schemas.pydantic_schemas.pagination import PaginationTemplate


async def pagination_mixin(
    page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)
):
    pagination_data = PaginationTemplate(page=page, size=size)
    return pagination_data
