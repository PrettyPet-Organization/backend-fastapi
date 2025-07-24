from pydantic import BaseModel
from datetime import datetime

class IdMixin(BaseModel):
    id: int

class LevelVitalTemplate(
    IdMixin,
    BaseModel
):
    name: str


class SkillsVitalTemplate(
    IdMixin,
    BaseModel
):
    name: str


class SkillsResponseTemplate(BaseModel):
    message: str
    skill: SkillsVitalTemplate


class UserAdditionalDataMIxin(
    BaseModel
):
    level: LevelVitalTemplate | None
    skills: list[SkillsVitalTemplate] | None
    

class DateTimeMixin(
    BaseModel
):
    created_at: datetime
    updated_at: datetime


class BasicUserDataMixin(
    BaseModel
):
    email: str
    full_name: str | None
    bio: str | None
    preferences: str | None
    experience: str | None



class UserPutTemplate(
    BasicUserDataMixin,
    DateTimeMixin,
    BaseModel
):
    pass


class UserCompleteDataTemplate(
    IdMixin,
    BasicUserDataMixin,
    DateTimeMixin,
    UserAdditionalDataMIxin,
    BaseModel
):
    pass


# class UserDataPublicTemplate(
#     BasicUserDataTemplate,
#     UserAdditionalData,
#     BaseModel
# ):
#     pass

