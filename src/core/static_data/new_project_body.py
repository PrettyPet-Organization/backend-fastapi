from core.schemas.pydantic_shcemas.project_schemas import BasicProjectTemplate 


async def new_project_mail_body(
    project_data: BasicProjectTemplate
) -> str:
    new_project_message = (
f"""
Проект просит быть добавленным: {project_data.title}
описание проекта:
{project_data.description}
""")
    return new_project_message
