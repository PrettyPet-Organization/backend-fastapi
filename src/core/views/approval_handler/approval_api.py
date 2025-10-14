from core.schemas.pydantic_shcemas.response_schemas import ApplicationResponseTemplate
from core.schemas.pydantic_shcemas.project_schemas import ProjectRolesResponsesTemplate
from core.schemas.pydantic_shcemas.action_schemas import ActionTemplate
from typing import Annotated
from core.models.user_models import (
    ProjectRoleUsersAssociation,
    ProjectRoleResponseBase,
    ProjectRolesBase,
    ProjectBase,
    UsersBase
)
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from core.dependencies.auth import (
    get_current_user,
    get_db
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Query
)
from sqlalchemy import (
    select,
    delete,
    update
)
from sqlalchemy.orm import (
    joinedload,
    selectinload
)


approval_router = APIRouter(prefix = "/api/v1")


@approval_router.get("/application/retreive/user/{user_id}", response_model = list[ApplicationResponseTemplate])
async def retreive_users_applications(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
):
    if user_id != user_data.id:
        raise HTTPException(
            status_code = 403,
            detail = "Only the user applied is allowed to view the applications"
        )

    stmt = (
        select(
           ProjectRoleResponseBase 
        )
        .where(
            ProjectRoleResponseBase.user_id == user_data.id
        )
    )
    applications = await db.execute(stmt)
    applications = applications.scalars().all()

    return applications


@approval_router.get("/application/retreive/project/{project_id}", response_model = ProjectRolesResponsesTemplate)
async def retrieve_project_applictaions(
    project_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)]
):
    stmt = (
        select(
            ProjectBase
        )
        .options(
            joinedload(ProjectBase.roles)
                .joinedload(ProjectRolesBase.project_role_response)
        )
        .where(
            ProjectBase.id == project_id,
        )
    )
    
    project_data = await db.execute(stmt)
    project_data = project_data.unique().scalar_one_or_none()

    if not project_data:
        raise HTTPException(
            status_code = 404,
            detail = "No such project exists"
        )
    if not project_data.creator_id == user_data.id:
        raise HTTPException(
            status_code = 403,
            detail = "Only the creator is allowed to view who has applied to the project"
        )

    return project_data


@approval_router.post("/application/{role_id}")
async def apply_for_a_position(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    role_id: int
):
    stmt = (
        select(
            ProjectRolesBase
        )
        .where(
            ProjectRolesBase.id == role_id
        )
    )

    role_existance = await db.execute(stmt)
    role_existance = role_existance.scalar_one_or_none()

    if not role_existance:
        raise HTTPException(
            status_code = 404,
            detail = "The role you are trying to apply for is absent in the database."
        )
    if role_existance.number_of_needed <= 0:
        raise HTTPException(
            status_code = 403,
            detail = "The project has no spare role for you"
        )
    
    application = ProjectRoleResponseBase(
        project_role_id = role_id,
        user_id = user_data.id
    )

    db.add(application)
    await db.commit()
    await db.refresh(application)

    return Response(
        status_code = 201,
        content = "You have applied for the project "
    )


@approval_router.post("/application/review/{application_id}", response_model = ProjectRolesResponsesTemplate)
async def review_application(
    application_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    action: ActionTemplate
):
    stmt = (
        select(
            ProjectRoleResponseBase
        )
        .options(
            joinedload(ProjectRoleResponseBase.project_role)
                .joinedload(ProjectRolesBase.project)
        )
        .where(
            ProjectRoleResponseBase.id == application_id
        )
    )

    application = await db.execute(stmt)
    application = application.scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code = 404,
            detail = "There is no application going by such id"
        )
    
    if user_data.id != application.project_role.project.creator_id:
        raise HTTPException(
            status_code = 403,
            detail = "You are not allowed to approve people for roles"
        )

    match action.action:
        case "accept":
            stmt = (
                update(
                    ProjectRolesBase
                )
                .where(
                    ProjectRolesBase.id == application.project_role.id
                )
                .values(
                    number_of_needed = application.project_role.number_of_needed - 1
                )
            )

            new_association = ProjectRoleUsersAssociation(
                project_role_id = application.project_role_id,
                users_id = application.user_id
            )

            db.add(new_association)
            await db.execute(stmt)
            await db.flush()


            stmt = (
                update(
                    ProjectRoleResponseBase
                )
                .where(
                    ProjectRoleResponseBase.id == application_id
                )
                .values(
                    application_status = "approved",
                    response_text = action.response_text,
                    reviewed_at = datetime.now(),
                    reviewed_by_user_id = user_data.id 
                )   
            )
        case "decline":
            stmt = (
                update(
                    ProjectRoleResponseBase
                )
                .where(
                    ProjectRoleResponseBase.id == application_id
                )
                .values(
                    application_status = "declined",
                    response_text = action.response_text,
                    reviewed_at = datetime.now(),
                    reviewed_by_user_id = user_data.id 
                )
            )
        case _:
            raise HTTPException(
                status_code = 400,
                detail = "Incorrect action"
            )
        
    await db.execute(stmt)
    await db.commit()
    await db.refresh(application)

    return application


@approval_router.delete("/application/delete/{application_id}", response_model = ProjectRolesResponsesTemplate)
async def resign_from_project(
    db: Annotated[AsyncSession, Depends(get_db)],
    user_data: Annotated[UsersBase, Depends(get_current_user)],
    application_id: int
):
    stmt = (
        select(
            ProjectRoleResponseBase
        )
        .options(
            joinedload(ProjectRoleResponseBase.project_role)
                .joinedload(ProjectRolesBase.project)
        )
        .where(
            ProjectRoleResponseBase.id == application_id 
        )
    )

    application = await db.execute(stmt)
    application = application.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=404,
            detail = "There is no such application"
        )
    if user_data.id not in [application.project_role.project.creator_id, application.user_id]:
        raise HTTPException(
            status_code = 403,
            detail = "Only the applied user and the project creator are allowed to delete the application"
        )

    if application.application_status == "approved":
        stmt = (
            delete(
                ProjectRoleResponseBase
            )
            .where(
                ProjectRoleResponseBase.id == application_id
            )
        )

        await db.execute(stmt)
        await db.flush()

        stmt = (
            update(
                ProjectRolesBase
            )
            .values(
                number_of_needed = application.project_role.number_of_needed + 1
            )
            .where(
                ProjectRolesBase.id == application.project_role_id
            )
        )

        await db.execute(stmt)
        await db.commit()

        return Response(
            status_code = 204
        )

    else:
        stmt = (
            delete(
                ProjectRoleResponseBase
            )
            .where(
                ProjectRoleResponseBase.id == application_id
            )
        )
        await db.execute(stmt)
        await db.commit()

        return Response(
            status_code = 204
        )
