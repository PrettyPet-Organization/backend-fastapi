from pydantic import BaseModel
from typing import Any, Dict


def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize()
                                   for word in components[1:])


class CamelCaseModel(BaseModel):
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        return {to_camel_case(k): v for k, v in data.items()}
