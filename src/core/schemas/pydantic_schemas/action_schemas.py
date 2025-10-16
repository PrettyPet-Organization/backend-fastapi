from enum import Enum

from pydantic import Field

from core.schemas.base import CamelBaseModel


class ActionEnum(str, Enum):
    DECLINE = "decline"
    ACCEPT = "accept"


class ActionTemplate(CamelBaseModel):
    action: ActionEnum
    response_text: str | None
