from datetime import datetime
from typing import Annotated

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, mapped_column


class IntPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class CreatedAtMixin:
    created_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]


class UpdatedAtMixin:
    updated_at: Mapped[
        Annotated[
            datetime, mapped_column(server_default=func.now(), onupdate=func.now())
        ]
    ]

class AssignedAtMixin:
    assigned_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]


class Base(DeclarativeBase, IntPkMixin):
    pass


def get_str_field(
    length: int | None = 256, collation: str | None = None
) -> MappedColumn[String]:
    """Generate SQLAlchemy `mapped_column` for string fields.

    Need to avoid repetitive `mapped_column(String(256))` in models.

    Usage:
    ```
    from typing import Annotated

    from fastapi import Depends
    from sqlalchemy import String
    from sqlalchemy.orm import Mapped, mapped_column

    class SomeModel:
        some_str_field: Mapped[Annotated[str, Depends(get_str_field)]].
    ```.
    """
    return mapped_column(String(length=length, collation=collation))


def get_str_field_nullable(
    length: int | None = 256, collation: str | None = None
):
    return mapped_column(String(length=length, collation=collation, nullable = True))
