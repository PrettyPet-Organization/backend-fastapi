from pydantic import BaseModel


class IdMixin(BaseModel):
    id: int


class RoleTypeMixin(BaseModel):
    name: str


class RoleTypeTemplate(
    RoleTypeMixin,
    IdMixin,
    BaseModel
):
    pass

# class 

class BasicRoleTemplate(BaseModel):
    role_type: RoleTypeTemplate 
    project_id: int
    description: str
    required_skills_description: str
    number_of_needed: int


class CompleteRoleTemplate(BasicRoleTemplate, BaseModel):
    id: int


class RoleInput(BaseModel):
    description: str
    required_skills_description: str
    number_of_needed: int