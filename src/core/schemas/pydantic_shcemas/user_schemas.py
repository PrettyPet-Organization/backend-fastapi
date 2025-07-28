from pydantic import BaseModel
from datetime import datetime

class LevelTemplate(BaseModel):
    id: int
    name: str


class SkillsTemplate(BaseModel):
    id: int
    name: str


class SkillsWithMessageTemplate(BaseModel):
    id: int
    name: str
    message: str = "Skill added successfully"


class UserOutputTemplate(BaseModel):
    id: int
    email: str
    full_name: str | None
    bio: str | None
    preferences: str | None
    experience: str | None
    created_at: datetime 
    updated_at: datetime

    level: LevelTemplate | None
    skills: list[SkillsTemplate] | None


class PutUserTemplate(BaseModel):
    email: str | None
    full_name: str | None
    bio: str | None
    preferences: str | None