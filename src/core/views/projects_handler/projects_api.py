import logging
import os
from typing import Annotated

from fastapi import (APIRouter, Depends, HTTPException, Path, Query, Response,
                     Security)
from fastapi.responses import JSONResponse
from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.dependencies.auth import get_current_user, get_db
from core.models.user_models import ProjectBase, ProjectRolesBase, UsersBase
from core.schemas.pydantic_schemas.pagination import PaginationTemplate
from core.schemas.pydantic_schemas.project_schemas import (
    BasicProjectTemplate, ProjectTemplateShort, ProjectTemplateWithRoles)
from core.static_data.new_project_body import new_project_mail_body
from core.static_data.new_project_subject import new_project_mail_subject
from core.utils.pagination_mixin import pagination_mixin
from core.utils.send_email import send_email

projects_router = APIRouter(prefix="/api/v1")


@projects_router.post("/projects", status_code=201, response_model=ProjectTemplateShort)
async def create_project(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Security(get_current_user)],
    new_project_data: BasicProjectTemplate,
) -> ProjectBase:
    new_project = ProjectBase(
        **(new_project_data.model_dump()), creator_id=user_data.id
    )

    db.add(new_project)
    await db.commit()

    await db.refresh(new_project)

    message_body = await new_project_mail_body(new_project)
    message_subject = await new_project_mail_subject(new_project)

    await send_email(
        message_receiver=os.getenv("SENDER_EMAIL"),
        message_body=message_body,
        message_subject=message_subject,
    )

    return new_project


@projects_router.get(
    "/projects", status_code=200, response_model=list[ProjectTemplateWithRoles]
)
async def get_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: PaginationTemplate = Depends(pagination_mixin),
    query_filter: str | None = "",
) -> ProjectBase:
    page = pagination.page if pagination.page else 1
    size = pagination.size if pagination.size else 10

    if query_filter:
        tsvector = func.to_tsvector(
            "simple", ProjectBase.title + " " + ProjectBase.description
        )
        tsquery = func.plainto_tsquery("simple", query_filter)

        rank = func.ts_rank(tsvector, tsquery)

        stmt = (
            select(ProjectBase, rank.label("rank"))
            .options(
                selectinload(ProjectBase.roles).joinedload(ProjectRolesBase.role_types)
            )
            .where(tsvector.op("@@")(tsquery))
            .order_by(desc(rank))
            .limit(size)
            .offset((page - 1) * size)
        )
    else:
        stmt = (
            select(ProjectBase)
            .options(
                selectinload(ProjectBase.roles).joinedload(ProjectRolesBase.role_types)
            )
            .order_by(desc(ProjectBase.created_at))
            .limit(size)
            .offset((page - 1) * size)
        )

    projects_filtered = await db.execute(stmt)
    projects_filtered_scalared = projects_filtered.scalars()

    return projects_filtered_scalared


@projects_router.get(
    "/projects/{project_id}", status_code=200, response_model=ProjectTemplateWithRoles
)
async def retreive_project_by_id(
    db: Annotated[AsyncSession, Depends(get_db)], project_id: int = Path(ge=1)
) -> ProjectBase:
    stmt = (
        select(ProjectBase)
        .options(
            selectinload(ProjectBase.roles).selectinload(ProjectRolesBase.skills),
            selectinload(ProjectBase.roles).selectinload(ProjectRolesBase.role_types),
            selectinload(ProjectBase.roles).selectinload(ProjectRolesBase.users),
        )
        .where(ProjectBase.id == project_id)
    )

    response_model = await db.execute(stmt)
    response = response_model.scalar_one_or_none()
    if not response:
        raise HTTPException(detail="There was no such project found", status_code=404)
    return response


@projects_router.delete("/projects/{project_id}", status_code=204)
async def delete_project(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
) -> JSONResponse:
    stmt = select(ProjectBase).where(ProjectBase.id == project_id)
    project_data = await db.execute(stmt)
    project_data = project_data.scalar_one_or_none()

    if not project_data:
        raise HTTPException(status_code=404, detail="There is no project with such id")
    if project_data.creator_id != user_data.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete someone else's projects",
        )

    try:
        stmt = delete(ProjectBase).where(ProjectBase.id == project_id)
        data_on_delete = await db.execute(stmt)
        await db.commit()
        logging.info(data_on_delete)
        return Response(status_code=204)

    except Exception as e:
        logging.warning(e)
        raise HTTPException(status_code=500, detail="something went wrong")


@projects_router.put(
    "/projects/{project_id}", status_code=201, response_model=ProjectTemplateWithRoles
)
async def change_project(
    new_project_data: BasicProjectTemplate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    project_id: int = Path(ge=1),
) -> ProjectBase:
    stmt = (
        select(ProjectBase)
        .options(
            joinedload(ProjectBase.creator),
            selectinload(ProjectBase.roles).selectinload(ProjectRolesBase.role_types),
        )
        .where(ProjectBase.id == project_id)
    )

    project_data = await db.execute(stmt)

    project_data_scalar = project_data.scalar_one_or_none()

    if not project_data_scalar:
        raise HTTPException(status_code=404, detail="No project with such id was found")
    if project_data_scalar.creator_id != user_data.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to change data in the project"
        )

    stmt = (
        update(ProjectBase)
        .where(ProjectBase.id == project_id)
        .values(**(new_project_data.model_dump()))
    )

    await db.execute(stmt)

    await db.commit()

    await db.refresh(project_data_scalar)

    return project_data_scalar
