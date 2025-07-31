from .pydantic_mixins import (
    IdMixin
)
from pydantic import (
    Field,
    BaseModel
)



class BasicLevelTemplate(
    IdMixin,
    BaseModel
):
    name: str = Field(min_length = 4, max_length = 255)


class BasicRoleTemplate(
    IdMixin,
    BaseModel
): 
    name: str = Field(min_length = 4, max_length = 255)

class BasicSkillsTemplate(
    IdMixin,
    BaseModel
):
    name: str = Field(min_length = 4, max_length = 255)