from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base, CreatedAtMixin, UpdatedAtMixin, get_str_field


class User(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=True)

    oauth_provider: Mapped[Optional[str]] = mapped_column(nullable=True)
    oauth_id: Mapped[Optional[str]] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
