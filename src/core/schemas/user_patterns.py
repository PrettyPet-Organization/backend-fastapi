from pydantic import BaseModel
from datetime import datetime


class LevelVitalTemplate(BaseModel):
    id: int
    name: str


class SkillsVitalTemplate(BaseModel):
    id: int
    name: str


class UserDataPublicTemplate(BaseModel):
    id: int
    email: str
    full_name: str
    bio: str
    preferences: str
    experience: str
    created_at: datetime
    updated_at: datetime

    level: LevelVitalTemplate
    skills: list[SkillsVitalTemplate]


