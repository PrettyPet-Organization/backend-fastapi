from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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


class Base(DeclarativeBase, IntPkMixin):
    pass


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    """Комбинированный миксин для created_at + updated_at."""

    pass


class SoftDeleteMixin:
    """Мягкое удаление."""

    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
