from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.responses import (
    JSONResponse
)
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.user_models import (
    UsersBase,
    ProjectRolesBase,
    SkillsBase,
    UserSkillsAssociation,
    ProjectRolesBase,
    ProjectBase,
    ProjectRolesBase,
    ProjectRoleUsersAssociation,
    ProjectRoleSkillsAssociation
)
from core.dependencies.auth import (
    get_db,
    get_current_user
)
from sqlalchemy import (
    select,
    update,
    delete,
    and_
)
from sqlalchemy.orm import (
    joinedload,
    selectinload,
)



skills_router = APIRouter()


@skills_router.post("/api/v1/project_roles/{role_id}/skills/{skill_id}")
async def skill_data(
    role_id: int,
    skill_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
):
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
    elif project_data.project_id != user_data.id:
        raise HTTPException(detail="You are not allowed to change this data", status_code=403)


    new_role = ProjectRoleSkillsAssociation(
        role_id = role_id,
        skill_id = skill_id
    )
    
    await db.add(new_role)
    await db.commit()

    await db.refresh(project_data)

    return JSONResponse(
        content = {
            "message": "Skill added to role successfully",
            "role_id": project_data.id,
            "skill": project_data.skills
        }
    )


@skills_router.delete("/api/v1/project_roles/{role_id}/skills/{skill_id}", status_code = 204)
async def delete_skill_connection(
    role_id: int,
    skill_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> JSONResponse:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            selectinload(ProjectRolesBase.role_types),
            joinedload(ProjectRolesBase.project)
        )
        .where(ProjectRolesBase.id == role_id)
    )

    role_data = await db.execute(stmt)
    role_data = role_data.scalar_one_or_none()

    if not role_data:
        raise HTTPException(status_code = 404, detail = "Either the project or the role was not found")
    elif role_data.project.creator_id != user_data.id:
        raise HTTPException(status_code=403, detail = "You are not allowed to make such changes")

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
