from fastapi import APIRouter, Security

from core.utils.health_check.views import router as health_check_router
from core.views.auth import router as auth_router, bearer_scheme

router = APIRouter()

router.include_router(health_check_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])

