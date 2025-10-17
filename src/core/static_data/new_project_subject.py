from core.models.user_models import ProjectBase
from core.schemas.pydantic_schemas.project_schemas import BasicProjectTemplate


async def new_project_mail_subject(project_data: ProjectBase) -> str:

    subject = f"Новый проект: {project_data.title}"

    return subject
