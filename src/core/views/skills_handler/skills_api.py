from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.dependencies.auth import get_current_user, get_db
from core.models.user_models import (
    ProjectRolesBase,
    ProjectRoleSkillsAssociation,
    SkillsBase,
    UsersBase,
)


skills_router = APIRouter(prefix = "/api/v1")


@skills_router.post("/project_roles/{role_id}/skills/{skill_id}")
async def skill_data(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    role_id: int = Path(ge=1),
    skill_id: int = Path(ge=1)
) -> JSONResponse:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            joinedload(ProjectRolesBase.project),
            selectinload(ProjectRolesBase.skills)
        )
        .where(
            ProjectRolesBase.id == role_id
        )
    )

    project_data = await db.execute(stmt)
    project_data = project_data.scalar_one_or_none()

    if not project_data:
        raise HTTPException(status_code = 404, detail = "Such role was not found")
    if project_data.project_id != user_data.id:
        raise HTTPException(detail="You are not allowed to change this data", status_code=403)
    if skill_id in [i.id for i in project_data.skills]:
        raise HTTPException(status_code = 409, detail = "This connection was already present in the database")

    stmt = (
        select(SkillsBase)
        .where(
            SkillsBase.id == skill_id
        )
    )

    is_skill_present = await db.execute(stmt)
    is_skill_present = is_skill_present.scalar_one_or_none()
    if not is_skill_present:
        raise HTTPException(status_code=404, detail = "No skill matched given id")


    new_role = ProjectRoleSkillsAssociation(
        role_id = role_id,
        skill_id = skill_id
    )

    db.add(new_role)
    await db.commit()

    await db.refresh(project_data)

    return JSONResponse(
        status_code = 201,
        content = {
            "message": "Skill added to role successfully",
            "role_id": project_data.id,
            "skill": {i.id: i.name for i in project_data.skills}
        }
    )


@skills_router.delete("/project_roles/{role_id}/skills/{skill_id}", status_code = 204)
async def delete_skill_connection(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    role_id: int = Path(ge=1),
    skill_id: int = Path(ge=1)
) -> JSONResponse:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            selectinload(ProjectRolesBase.role_types),
            joinedload(ProjectRolesBase.project)
        )
        .where(
            ProjectRolesBase.id == role_id
        )
    )

    role_data = await db.execute(stmt)
    role_data = role_data.scalar_one_or_none()

    if not role_data:
        raise HTTPException(status_code = 404, detail = "Either the project or the role was not found")
    if role_data.project.creator_id != user_data.id:
        raise HTTPException(status_code=403, detail = "You are not allowed to make such changes")

    stmt = (
        select(ProjectRoleSkillsAssociation)
        .where(
            and_(
                ProjectRoleSkillsAssociation.role_id == role_id,
                ProjectRoleSkillsAssociation.skill_id == skill_id
            )
        )
    )
    is_existing = await db.execute(stmt)
    is_existing = is_existing.scalar_one_or_none()

    if not is_existing:
        raise HTTPException(status_code=409, detail = "There was no such connection in the first place")

    stmt = (
        delete(ProjectRoleSkillsAssociation)
        .where(
            and_(
                ProjectRoleSkillsAssociation.role_id == role_id,
                ProjectRoleSkillsAssociation.skill_id == skill_id
            )
        )
    )

    await db.execute(stmt)
    await db.commit()

    return JSONResponse(
        content = {},
        status_code = 204
    )
