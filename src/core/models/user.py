
# from sqlalchemy.orm import Mapped, mapped_column

# from core.models.base import Base, CreatedAtMixin, UpdatedAtMixin


# class User(Base, CreatedAtMixin, UpdatedAtMixin):
#     __tablename__ = "users"

#     email: Mapped[str] = mapped_column(unique=True, index=True)
#     hashed_password: Mapped[str | None] = mapped_column(nullable=True)

#     oauth_provider: Mapped[str | None] = mapped_column(nullable=True)
#     oauth_id: Mapped[str | None] = mapped_column(nullable=True)

#     is_active: Mapped[bool] = mapped_column(default=True)
