from pydantic import BaseModel
from fastapi import Query



class ListQueryTemplate(BaseModel):
    page: int = Query(1, ge = 1)
    size: int = Query(10, ge=1, le=100)


class FilterQueryTemplate(BaseModel):
    filter: str = Query()