from pydantic import BaseModel
from decimal import Decimal


class RoleTypeTemplate(BaseModel):
    id: int
    name: str

class NewProjectTemplate(BaseModel):
    title: str
    description: str
    desired_fundraising_amount: Decimal
    entry_ticket_price: Decimal


class CreatorTemplate(BaseModel):
    id: int 
    


class RoleTemplate(BaseModel):
    id: int
    required_skills_description: str
    number_of_needed: int
    role_types: RoleTypeTemplate


class ProjectTemplateV2(BaseModel):
    id: int | None
    title: str | None
    description: str | None
    desired_fundraising_amount: Decimal | None
    entry_ticket_price: Decimal | None
    creator_id: int | None
    roles: list[RoleTemplate] | None


class ProjectTemplateShort(BaseModel):
    id: int
    title: str | None
    description: str | None
    desired_fundraising_amount: Decimal | None
    entry_ticket_price: Decimal | None
    creator_id: int | None



# class ProjectOutputTemplate(BaseModel):
#     id: int
#     title: str
#     description: str
#     desired_fundraising_amount: float
#     entry_ticket_price: float

