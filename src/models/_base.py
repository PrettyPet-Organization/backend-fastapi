from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, mapped_column


IntPK = Annotated[int, mapped_column(primary_key=True)]
UUIDPK = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
CreatedAt = Annotated[datetime, mapped_column(default=datetime.now)]
UpdatedAt = Annotated[
    datetime, mapped_column(default=datetime.now, onupdate=datetime.now)
]
UniqueStr = Annotated[str, mapped_column(unique=True)]


class Base(DeclarativeBase):
    pass
