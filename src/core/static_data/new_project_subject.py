from core.schemas.pydantic_shcemas.project_schemas import BasicProjectTemplate 
from core.models.user_models import ProjectBase

async def new_project_mail_subject(
    project_data: ProjectBase
) -> str:
    
    subject  = f"Новый проект: {project_data.title}"
    
    return subject

