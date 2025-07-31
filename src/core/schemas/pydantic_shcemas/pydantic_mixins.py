from pydantic import Field, BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated

class IdMixin(BaseModel):
    id: int = Field(ge=1)


class DateTimeMixin(BaseModel):
    created_at: datetime 
    updated_at: datetime


class BasicUserDataMixin(BaseModel):
    full_name: str | None = Field(min_length = 4, max_length = 255)
    bio: str | None
    preferences: str | None = Field(min_length = 4, max_length = 1000)
    experience: str | None = Field(min_length = 4, max_length = 1000)


class RoleTypeMixin(BaseModel):
    id: int = Field(ge = 1)
    name: str = Field(max_length = 255)


class ProjectEssentialsMixin(BaseModel):
    title: str | None = Field(min_length = 4, max_length = 255)
    description: str | None = Field(min_length = 4, max_length = 1000)


class DecimalProjectMixin(BaseModel):
    desired_fundraising_amount: Decimal | None = Field(ge = 0, decimal_places = 2, max_digits = 10)
    entry_ticket_price: Decimal | None = Field(ge = 0, decimal_places = 2, max_digits = 10)


class EmailMixin(BaseModel):
    email: EmailStr

class RoleEssentialsMixin(BaseModel):
    description: str | None = Field(min_length = 6)
    required_skills_description: str | None = Field(min_length = 4)
    number_of_needed: int | None = Field(ge = 0)