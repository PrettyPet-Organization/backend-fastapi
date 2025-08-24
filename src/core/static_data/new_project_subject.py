from core.schemas.pydantic_shcemas.project_schemas import BasicProjectTemplate 


async def new_project_mail_subject(
    project_data: BasicProjectTemplate
) -> str:
    
    subject = (
f"""
New project pending: {project_data.title}
"""
    )

    return subject

