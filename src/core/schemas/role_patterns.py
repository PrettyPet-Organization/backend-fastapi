from pydantic import BaseModel


class BasicRoleTemplate(BaseModel):
    role_type: dict # this should be another thing 
    project_id: int
    description: str
    required_skills_description: str
    number_of_needed: int


class CompleteRoleTemplate(BasicRoleTemplate, BaseModel):
    id: int