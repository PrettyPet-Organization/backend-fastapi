from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response
from fastapi.responses import JSONResponse
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.dependencies.auth import get_current_user, get_db
from core.models.user_models import (
    ProjectBase,
    ProjectRolesBase,
    RoleTypesBase,
    UsersBase,
)
from core.schemas.pydantic_shcemas.role_schemas import (
    RoleExtendedOutputTemplate,
    RoleInputTemplate,
    RoleOutputTemplate,
)


roles_router = APIRouter(prefix = "/api/v1")


@roles_router.post("/projects/{project_id}/roles/{role_id}", status_code = 201, response_model=RoleOutputTemplate)
async def add_role_to_the_project(
    new_role_data: RoleInputTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
    role_id: int = Path(ge=1),
) -> ProjectRolesBase:

    stmt = (
        select(RoleTypesBase)
        .where(
            RoleTypesBase.id == role_id
        )
    )

    role_in_the_database = await db.execute(stmt)
    role_in_the_database = role_in_the_database.scalar_one_or_none()
    if not role_in_the_database:
        raise HTTPException(status_code = 404, detail = "There was no such role type found in the database")

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

    stmt = (
        select(ProjectRolesBase)
        .where(
            and_(
                ProjectRolesBase.role_type_id == role_id,
                ProjectRolesBase.project_id == project_id
            )
        )
    )

    is_existing_connection = await db.execute(stmt)
    is_existing_connection = is_existing_connection.scalar_one_or_none()

    if is_existing_connection:
        raise HTTPException(status_code = 409, detail = "This role already is required in the project")

    new_role = ProjectRolesBase(
        role_type_id = role_id,
        project_id = project_id,
        **(new_role_data.model_dump())
    )
    db.add(new_role)
    await db.commit()

    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            joinedload(ProjectRolesBase.role_types)
        )
        .where(
            ProjectRolesBase.role_type_id == role_id,
            ProjectRolesBase.project_id == project_id
        )
    )

    return_data = await db.execute(stmt)
    return_data = return_data.scalar_one_or_none()

    return return_data



@roles_router.get("/projects/{project_id}/roles", status_code = 200, response_model = list[RoleOutputTemplate])
async def get_project_roles(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
) -> list[ProjectRolesBase]:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            joinedload(ProjectRolesBase.role_types)
        )
        .where(
            ProjectRolesBase.project_id == project_id
        )
    )
    roles_data = await db.execute(stmt)

    roles_data = roles_data.scalars().all()

    if not roles_data:
        raise HTTPException(status_code = 404, detail = "No project with such id was found")

    return roles_data


@roles_router.put("/projects/{project_id}/roles/{role_id}", status_code = 201, response_model = RoleExtendedOutputTemplate)
async def change_project_role(
    project_role_data: RoleInputTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
    role_id: int = Path(ge=1),
) -> ProjectRolesBase:
    stmt = (
        select(
            ProjectRolesBase
        )
        .options(
            joinedload(ProjectRolesBase.project)
                .joinedload(ProjectBase.creator),
            joinedload(ProjectRolesBase.role_types)
        )
        .where(
            and_(
                ProjectRolesBase.project_id == project_id,
                ProjectRolesBase.role_type_id == role_id
            )
        )
    )

    role_info = await db.execute(stmt)
    role_info_scalar = role_info.scalar_one_or_none()

    if not role_info_scalar:
        raise HTTPException(status_code = 404, detail = "There was no such role found in the project")
    if role_info_scalar.project.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change data here")
    if not role_id == role_info_scalar.id:
        raise HTTPException(status_code = 404, detail = "The role was not found in the project")

    stmt = (
        update(ProjectRolesBase)
        .values(
            **(project_role_data.model_dump())
        )
        .where(
            and_(
                ProjectRolesBase.role_type_id == role_id,
                ProjectRolesBase.project_id == project_id
            )
        )
    )

    await db.execute(stmt)
    await db.commit()

    await db.refresh(role_info_scalar)

    return role_info_scalar



@roles_router.delete("/projects/{project_id}/roles/{role_id}", status_code = 204)
async def delete_role(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
    role_id: int = Path(ge=1),
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
    if project_data.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change data for someone else's project" )

    stmt = (
        select(RoleTypesBase)
        .where(
            RoleTypesBase.id == role_id
        )
    )

    is_role_existing = await db.execute(stmt)
    is_role_existing = is_role_existing.scalar_one_or_none()

    if not is_role_existing:
        raise HTTPException(status_code = 404, detail = "There was no such role in the database")

    stmt = (
        select(ProjectRolesBase)
        .where(
            and_(
                ProjectRolesBase.role_type_id == role_id,
                ProjectRolesBase.project_id == project_id
            )
        )
    )

    is_existing_connection = await db.execute(stmt)
    is_existing_connection = is_existing_connection.scalar_one_or_none()

    if not is_existing_connection:
        raise HTTPException(status_code = 409, detail = "There was already no such connetcion in the database")

    stmt = (
        delete(
            ProjectRolesBase
        )
        .where(
            and_(
                ProjectRolesBase.project_id == project_id,
                ProjectRolesBase.role_type_id == role_id
            )
        )
    )

    await db.execute(stmt)
    await db.commit()

    return Response(status_code = 204)
