from .pydantic_mixins import (
    IdMixin
)
from pydantic import (
    BaseModel,
    Field
)



class BasicLevelTemplate(
    BaseModel,
    IdMixin
):
    name: str = Field(min_length = 4, max_length = 255)


class BasicRoleTemplate(
    BaseModel,
    IdMixin
): 
    name: str = Field(min_length = 4, max_length = 255)

class BasicSkillsTemplate(
    BaseModel,
    IdMixin
):
    name: str = Field(min_length = 4, max_length = 255)