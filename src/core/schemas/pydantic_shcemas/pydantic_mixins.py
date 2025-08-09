from datetime import datetime
from decimal import Decimal

from pydantic import EmailStr, Field

from core.schemas.base import CamelBaseModel


class IdMixin(CamelBaseModel):
    id: int = Field(ge=1)


class DateTimeMixin(CamelBaseModel):
    created_at: datetime
    updated_at: datetime


class BasicUserDataMixin(CamelBaseModel):
    full_name: str | None = Field(min_length = 4, max_length = 255)
    bio: str | None
    preferences: str | None = Field(min_length = 4, max_length = 1000)
    experience: str | None = Field(min_length = 4, max_length = 1000)


class RoleTypeMixin(CamelBaseModel):
    id: int = Field(ge = 1)
    name: str = Field(max_length = 255)


class ProjectEssentialsMixin(CamelBaseModel):
    title: str | None = Field(min_length = 4, max_length = 255)
    description: str | None = Field(min_length = 4, max_length = 1000)


class DecimalProjectMixin(CamelBaseModel):
    desired_fundraising_amount: Decimal | None = Field(ge = 0, decimal_places = 2, max_digits = 10)
    entry_ticket_price: Decimal | None = Field(ge = 0, decimal_places = 2, max_digits = 10)


class EmailMixin(CamelBaseModel):
    email: EmailStr

class RoleEssentialsMixin(CamelBaseModel):
    description: str | None = Field(min_length = 6)
    required_skills_description: str | None = Field(min_length = 4)
    number_of_needed: int | None = Field(ge = 0)
