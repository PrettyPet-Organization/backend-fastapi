from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.responses import (
    JSONResponse
)
from core.schemas.project_patterns import (
    ProjectImputableTemplate,
    RoleInputTemplate,
    ExtendedProjectTemplate
)
from core.schemas.role_patterns import (
    BasicRoleTemplate,
    CompleteRoleTemplate
)
from typing import Annotated
from core.dependencies.auth import (
    get_db,
    get_current_user
)
from core.models.user_models import (
    UsersBase,
    ProjectRolesBase,
    SkillsBase,
    UserSkillsAssociation,
    ProjectRolesBase,
    ProjectBase,
    ProjectRolesBase,
    ProjectRoleUsersAssociation
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    joinedload
)
from sqlalchemy import (
    select,
    update,
    delete
)


roles_router = APIRouter()


@roles_router.post("/api/v1/projects/{project_id}/roles/{role_id}", status_code = 201, response_model=CompleteRoleTemplate)
async def add_role_to_the_project(
    project_id: int,
    role_id: int,
    # new_role_data: BasicRoleTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> ProjectRolesBase:

    stmt = (
        select(
            ProjectBase
        )
        .where(
            ProjectBase.id == project_id
        )
    )

    project_data = await db.execute(stmt)
    project_data_scalar = project_data.scalar_one_or_none()

    if not project_data_scalar:
        raise HTTPException(status_code = 404, detail = "There was no project with such id in the database")
    if project_data_scalar.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "Only creator is allowed to add new roles to the project")
    
    # new_role = ProjectRolesBase(
    #     **(new_role_data.model_dump())
    # )
    new_role = ...
    await db.add(new_role)
    await db.commit()

    await db.refresh(project_data_scalar)

    return project_data_scalar


@roles_router.get("/api/v1/projects/{project_id}/roles", status_code = 200, response_model = list[CompleteRoleTemplate])
async def get_project_roles(
    project_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> list[ProjectRolesBase]:
    stmt = (
        select(
            ProjectBase
        )
        .options(
            joinedload(ProjectBase.roles)
        )
        .where(
            ProjectBase.id == project_id
        )
    )

    project_data = await db.execute(stmt)  

    project_data = project_data.scalar_one_or_none()

    if not project_data:
        raise HTTPException(status_code = 404, detail = "No project with such id was found")
    
    return project_data.roles

###

@roles_router.put("/api/v1/projects/{project_id}/roles/{role_id}", status_code = 201, response_model = ExtendedProjectTemplate)
async def change_project_role(
    project_id: int,
    role_id: int,
    project_role_data: RoleInputTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> ProjectRolesBase:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            joinedload(ProjectRolesBase.project)
                .joinedload(ProjectBase.creator)
        )
        .where(
            ProjectRolesBase.id == role_id
        )
    )

    role_info = await db.execute(stmt)
    role_info_scalar = role_info.scalar_one_or_none()

    if not role_info_scalar:
        raise HTTPException(status_code = 404, detail = "There was no such role found in the project")
    elif role_info_scalar.project.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change data here")

    stmt = (
        update(ProjectRolesBase)
        .values(
            **(project_role_data.model_dump())
        )
        .where(
            ProjectRolesBase.id == project_id
        )
    )

    await db.execute(stmt)
    await db.commit()
    
    await db.refresh(role_info_scalar)

    return role_info_scalar


###   
    
@roles_router.delete("/api/v1/projects/{project_id}/roles/{role_id}", status_code = 204)
async def delete_role(
    project_id: int,
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> JSONResponse:
    stmt = (
        select(
            ProjectBase
        )
        .options(
            joinedload(ProjectBase.creator)
        )
        .where(
            ProjectBase.id == project_id
        )
    )

    project_data = await db.execute(stmt)
    project_data = project_data.scalar_one_or_none()

    if not project_data:
        raise HTTPException(detail = "There was no such project in the database", status_code = 404)
    elif project_data.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change data for someone else's project" )

    stmt = (
        delete(
            ProjectRolesBase
        )
        .where(
            ProjectRolesBase.project_id == project_id
        )
    )

    await db.execute(stmt)
    await db.commit()

    return JSONResponse(
        content = {},
        status_code = 204
    )
    