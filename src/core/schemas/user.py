from pydantic import ConfigDict, EmailStr

from core.schemas.base import CamelBaseModel


class UserCreate(CamelBaseModel):
    email: EmailStr
    password: str


class UserRead(CamelBaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class UserLogin(CamelBaseModel):
    email: EmailStr
    password: str
