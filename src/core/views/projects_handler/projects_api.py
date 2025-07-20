import logging
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query
)
from src.core.dependencies.auth import (
    get_db,
    get_current_user
)
from src.core.models.user_models import (
    UsersBase,
    SkillsBase,
    UserSkillsAssociation,
    ProjectRolesBase,
    ProjectBase,
    ProjectRolesBase,
    ProjectRoleUsersAssociation
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from typing import Annotated
from src.core.schemas.project_patterns import (
    ProjectTemplate,
    ProjectImputableTemplate,
    ExtendedProjectTemplate,
)
from src.core.schemas.query_handler import (
    ListQueryTemplate
)
from sqlalchemy.orm import (
    joinedload,
    selectinload
)
from sqlalchemy import (
    insert,
    delete,
    select,
    or_,
    update,
    func
)


projects_router = APIRouter()


@projects_router.post("/api/v1/projects", status_code=201, response_model = ProjectTemplate)
async def create_project(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    new_project_data: ProjectImputableTemplate,
) -> ProjectBase:
    new_project = ProjectBase(
        **(new_project_data.model_dump()),
        creator_id = user_data.id
    )

    await db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    return new_project
        

@projects_router.get("/api/v1/projects", status_code = 200, response_model = ...)
async def get_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge = 1),
    size: int = Query(10, ge=1, le=100),
    query_filter: str | None = None
) -> ProjectBase:
    stmt = (
        select(
            ProjectBase
        )
        .options(
            selectinload(ProjectBase.roles)
        )
        .where(
            or_(
                ProjectBase.description.ilike(query_filter),
                ProjectBase.title.ilike(query_filter)
            )
        )
        .order_by(
            ...
        )
        .limit(size)
        .offset((page - 1) * size)
    )

    projects_filtered = await db.execute(stmt)
    projects_filtered_scalared = projects_filtered.scalars()

    return projects_filtered_scalared



@projects_router.get("/api/v1/projects/{project_id}", status_code = 200, response_model = ExtendedProjectTemplate)
async def retreive_project_by_id(
    project_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> ProjectBase:
    stmt = (
        select(ProjectBase)
        .options(
            selectinload(ProjectBase.roles)
                .selectinload(ProjectRolesBase.skills)
                .selectinload(ProjectRolesBase.users),
            joinedload(ProjectBase.creator)
        )
        .where(
            ProjectBase.id == project_id
        )
    )

    response_model = await db.execute(stmt)
    response = response_model.scalar_one_or_none()
    if not response:
        raise HTTPException(detail = "There was no such project found", status_code = 404)
    else:
        return response


@projects_router.delete("/api/v1/projects/{project_id}", status_code = 204)
async def delete_project(
    project_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> JSONResponse:
    stmt = (
        select(ProjectBase)
        .where(ProjectBase.id == project_id)
    )
    project_data = await db.execute(stmt)
    project_data = project_data.scalar_one_or_none()

    if not project_data:
        raise HTTPException(status_code = 404, detail = "There is no project with such id")
    elif project_data.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to delete someone else's projects")

    try:
        stmt = (
            delete(ProjectBase)
            .where(ProjectBase.id == project_id)
        )
        data_on_delete = await db.execute(stmt)
        await db.commit()
        logging.info(data_on_delete)
        return JSONResponse(
            content = {},
            status_code = 204
        )
    
    except Exception as e:
        logging.warning(e)
        raise HTTPException(
            status_code=500,
            detail = "something went wrong"
        )


@projects_router.put("/api/v1/projects/{project_id}", status_code = 201, response_model = ProjectTemplate)
async def change_project(
    project_id: int,
    new_project_data: ProjectImputableTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
) -> ProjectBase:
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

    project_data_scalar = project_data.scalar_one_or_none()
    
    if not project_data_scalar:
        raise HTTPException(status_code = 404, detail = "No project with such id was found")
    elif project_data_scalar.creator_id != user_data.id:
        raise HTTPException(status_code = 403, detail = "You are not allowed to change data in the project") 

    stmt = (
        update(
            ProjectBase
        )
        .where(
            ProjectBase.id == project_id
        )
        .values(
            **(new_project_data.model_dump())
        )
    )

    data = await db.execute(stmt)

    await db.commit()

    await db.refresh(project_data_scalar)

    return project_data_scalar

    
    