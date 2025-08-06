from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.dependencies.auth import get_current_user, get_db
from core.models.user_models import SkillsBase, UsersBase, UserSkillsAssociation
from core.schemas.pydantic_shcemas.extended_mixins import BasicSkillsTemplate
from core.schemas.pydantic_shcemas.user_schemas import (
    PutUserTemplate,
    SkillsWithMessageTemplate,
    UserOutputTemplate,
)


users_router = APIRouter(prefix = "/api/v1")


@users_router.get("/users/{users_id}", status_code = 200, response_model = UserOutputTemplate)
async def get_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    users_id: int = Path(ge=1)
) -> UsersBase:
    stmt = (
    select(UsersBase)
    .options(
        joinedload(UsersBase.level),
        selectinload(UsersBase.skills)
    )
    .where(
        UsersBase.id == users_id
    ))

    user_data = await db.execute(stmt)

    user_data = user_data.scalar_one_or_none()
    if user_data:
        return user_data
    raise HTTPException(
        detail = "There is no user with such id",
        status_code = 404
    )


@users_router.put("/users/{user_id}", status_code = 201, response_model = UserOutputTemplate)
async def update_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    data_to_update: PutUserTemplate,
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    user_id: int = Path(ge=1),
) -> UsersBase:
    if user_data.id != user_id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change this data")

    stmt = (
        update(UsersBase)
        .where(
            UsersBase.id == user_id
        )
        .values(
            id = user_id,
            **(data_to_update.model_dump())
        )
    )
    await db.execute(stmt)
    await db.commit()

    stmt = (
        select(
            UsersBase
        )
        .options(
            joinedload(UsersBase.level),
            selectinload(UsersBase.skills)
        )
        .where(
            UsersBase.id == user_id
        )
    )

    response_data = await db.execute(stmt)
    response_data = response_data.scalar_one_or_none()

    if not response_data:
        raise HTTPException(status_code = 404, detail = "No user with such id")

    return response_data


@users_router.get("/users/{user_id}/skills", status_code = 200, response_model = list[BasicSkillsTemplate])
async def get_skills(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: int = Path(ge=1)
) -> list[SkillsBase]:
    stmt = (
        select(UsersBase)
        .options(
            selectinload(UsersBase.skills)
        )
        .where(
            UsersBase.id == user_id
        )
    )

    user_data = await db.execute(stmt)
    user_data = user_data.scalar_one_or_none()

    if not user_data:
        raise HTTPException(status_code = 404, detail = "Such user was not found")
    return user_data.skills


@users_router.post("/users/{user_id}/skills/{skill_id}", status_code = 201, response_model = SkillsWithMessageTemplate)
async def add_skill(
    user: Annotated[UsersBase, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: int = Path(ge=1),
    skill_id: int = Path(ge=1)
) -> SkillsBase:
    if user.id != user_id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to add skills to this user")

    skill_add = UserSkillsAssociation(
        user_id = user_id,
        skill_id = skill_id
    )

    stmt = (
        select(SkillsBase)
        .where(
            SkillsBase.id == skill_id
        )
    )

    skill_to_add = await db.execute(stmt)
    skill_to_add = skill_to_add.scalar_one_or_none()

    if not skill_to_add:
        raise HTTPException(detail = "There is no skill with such id in the database", status_code = 404)

    db.add(skill_add)
    await db.commit()

    await db.refresh(skill_to_add)
    return skill_to_add


@users_router.delete("/users/{user_id}/skills/{skill_id}", status_code = 204)
async def delete_skill(
    user: Annotated[UsersBase, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    user_id: int = Path(ge=1),
    skill_id: int = Path(ge=1)
) -> JSONResponse:
    if user.id != user_id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to delete someone else's data, other than yours")

    stmt = (
        delete(UserSkillsAssociation)
        .where(
            UserSkillsAssociation.user_id == user_id,
            UserSkillsAssociation.skill_id == skill_id
        )
    )

    await db.execute(stmt)
    await db.commit()

    return Response(status_code = 204)
