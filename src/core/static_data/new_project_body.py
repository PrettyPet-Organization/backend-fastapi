from core.models.user_models import ProjectBase
from core.schemas.pydantic_schemas.project_schemas import BasicProjectTemplate


async def new_project_mail_body(project_data: ProjectBase) -> str:
    new_project_message = f"id: {project_data.id}\n"
    new_project_message += f"Название: {project_data.title}\n"
    new_project_message += f"Описание проекта: {project_data.description}\n\n"
    new_project_message += f"id создателя: {project_data.creator_id}"
    new_project_message += f"Цена участия: {project_data.entry_ticket_price}\n"
    new_project_message += (
        f"Цена приблизительная: {project_data.desired_fundraising_amount}\n\n"
    )
    new_project_message += f"Время создания проекта: {project_data.created_at}"

    return new_project_message
