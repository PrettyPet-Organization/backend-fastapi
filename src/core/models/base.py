from datetime import datetime
from typing import Annotated
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


intpk_field = Annotated[int, mapped_column(primary_key=True)]
created_at_field = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at_field = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=func.now())
]
str_256_field = Annotated[str, mapped_column(String(256))]


class BaseModel(DeclarativeBase):
    id: Mapped[intpk_field]
    created_at: Mapped[created_at_field]
    updated_at: Mapped[updated_at_field]
