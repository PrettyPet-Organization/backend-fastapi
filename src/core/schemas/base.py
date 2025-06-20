from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    """Converter snake_case in camelCase"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
