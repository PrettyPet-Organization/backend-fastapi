from fastapi import APIRouter

from core.utils.health_check.views import router as health_check_router
from core.views.auth.auth_handler import auth_router
from core.views.projects_handler.projects_api import projects_router
from core.views.roles_handler.roles_api import roles_router
from core.views.skills_handler.skills_api import skills_router
from core.views.users_handler.users_api import users_router


router = APIRouter()

router.include_router(health_check_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(projects_router, tags = ["project"])
router.include_router(roles_router, tags = ["roles"])
router.include_router(skills_router, tags = ["skills"])
router.include_router(users_router, tags = ["users"])
