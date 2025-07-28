from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response
)
from fastapi.responses import JSONResponse
from core.dependencies.auth import (
    get_db,
    get_current_user
)
from typing import Annotated
from core.models.user_models import (
    UsersBase,
    SkillsBase,
    UserSkillsAssociation
)
from sqlalchemy import (
    select,
    update,
    delete
)
from sqlalchemy.orm import (
    joinedload,
    selectinload
)
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas.user_patterns import (
    UserPutTemplate,
    SkillsVitalTemplate,
    SkillsResponseTemplate,
    UserCompleteDataTemplate
    # UserDataPublicTemplate,
    # BasicUserDataTemplate
)
from core.schemas.pydantic_shcemas.user_schemas import (
    UserOutputTemplate,
    SkillsTemplate,
    PutUserTemplate,
    SkillsWithMessageTemplate
)


users_router = APIRouter()


@users_router.get("/api/v1/users/{users_id}", status_code = 200, response_model = UserOutputTemplate)
async def get_user(
    users_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
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
    else:
        raise HTTPException(
            detail = "There is no user with such id",
            status_code = 404
        )
    

@users_router.put("/api/v1/users/{user_id}", status_code = 201, response_model = UserOutputTemplate)
async def update_user(
    user_id: int,
    data_to_update: PutUserTemplate,
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
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


@users_router.get("/api/v1/users/{user_id}/skills", response_model = list[SkillsTemplate])
async def get_skills(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> list[SkillsBase]:
    stmt = (
        select(SkillsBase)
        .where(
            SkillsBase.users.any(UsersBase.id == user_id)
        )
    )

    skills_data = await db.execute(stmt)
    skills_data = skills_data.scalars()

    return skills_data

### какая-то 

@users_router.post("/api/v1/users/{user_id}/skills/{skill_id}", response_model = SkillsWithMessageTemplate)
async def add_skill(
    user_id: int,
    skill_id: int,
    user: Annotated[UsersBase, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
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
        raise HTTPException(detail = "There is no skill with such id in the database", status_code = 400)
    
    db.add(skill_add)
    await db.commit()

    await db.refresh(skill_to_add)
    return skill_to_add


@users_router.delete("/api/v1/users/{user_id}/skills/{skill_id}", status_code = 204)
async def delete_skill(
    user_id: int,
    skill_id: int,
    user: Annotated[UsersBase, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
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
