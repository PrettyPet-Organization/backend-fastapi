from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ConfigDict,
    Field,
)
import re
from datetime import date as date_type


class UserProfileCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Обязательные поля
    profile_photo: str = Field(..., description="URL или base64 строка с фото профиля")
    main_stack: List[str] = Field(
        ..., min_items=1, description="Основной стек технологий"
    )

    # Необязательные поля
    resume: Optional[str] = Field(None, description="URL или base64 строка с резюме")
    hobbies: Optional[List[str]] = Field(None, description="Список увлечений")
    birth_date: Optional[date_type] = Field(None, description="Дата рождения")
    city: Optional[str] = Field(None, description="Город проживания")

    @field_validator("main_stack", "hobbies")
    @classmethod
    def validate_list_length(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        if v and len(v) > 20:
            raise ValueError("List cannot contain more than 20 items")
        return v

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: Optional[date_type]) -> Optional[date_type]:
        if v:
            if v > date_type.today():
                raise ValueError("Birth date cannot be in the future")
            # Проверка что пользователю хотя бы 13 лет
            age = (date_type.today() - v).days // 365
            if age < 13:
                raise ValueError("You must be at least 13 years old")
        return v

    @field_validator("profile_photo", "resume")
    @classmethod
    def validate_file_size(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) > 10 * 1024 * 1024:  # 10MB limit
            raise ValueError("File size too large")
        return v


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Обязательные поля
    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=8)]
    profile: UserProfileCreate

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?`~" for char in v):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        # Простая проверка домена
        if v.endswith((".ru", ".by")):
            # Можно добавить логику для определенных доменов
            pass
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    wallet_stars: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile: "UserProfileResponse"


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    profile_photo: str
    main_stack: List[str]
    resume: Optional[str] = None
    hobbies: Optional[List[str]] = None
    birth_date: Optional[date_type] = None
    city: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


UserResponse.model_rebuild()
