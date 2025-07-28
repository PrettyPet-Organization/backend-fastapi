from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class RoleTypeOutput(BaseModel):
    id: int
    name: str


class RoleOutputTemplate(BaseModel):
    id: int
    role_types: RoleTypeOutput | None
    project_id: int | None
    description: str | None
    required_skills_description: str | None
    number_of_needed: int | None


class RoleInputTemplate(BaseModel):
    description: str
    required_skills_description: str
    number_of_needed: int


class UserTemplateProto(BaseModel):
    id: int
    email: str
    full_name: str | None
    bio: str | None
    preferences: str | None
    experience: str | None
    created_at: datetime 
    updated_at: datetime


class ProjectTemplate(BaseModel):
    id: int
    title: str
    description: str
    desired_fundraising_amount: Decimal
    entry_ticket_price: Decimal
    creator: UserTemplateProto


class RoleExtendedOutputTemplate(BaseModel):
    id: int
    role_types: RoleTypeOutput | None
    project_id: int | None
    description: str | None
    required_skills_description: str | None
    number_of_needed: int | None

    project: ProjectTemplate
