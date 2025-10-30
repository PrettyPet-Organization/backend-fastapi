from fastapi import APIRouter

from core.utils.health_check.views import router as health_check_router
from core.views.approval_handler.approval_api import approval_router
from core.views.projects_handler.projects_api import projects_router
from core.views.roles_handler.roles_api import roles_router
from core.views.skills_handler.skills_api import skills_router
from core.views.users_handler.users_api import users_router

core_router = APIRouter()

# Health check
core_router.include_router(health_check_router, prefix="/health", tags=["System"])

# Main endpoints
core_router.include_router(projects_router, prefix="/projects", tags=["Projects"])
core_router.include_router(users_router, prefix="/users", tags=["Users"])
core_router.include_router(skills_router, prefix="/skills", tags=["Skills"])
core_router.include_router(roles_router, prefix="/roles", tags=["Roles"])
core_router.include_router(approval_router, prefix="/approval", tags=["Approval"])
