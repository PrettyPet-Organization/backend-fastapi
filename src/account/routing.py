from fastapi import APIRouter

from account.views.auth import router as auth_router
from account.views.registration import router as registration_router

account_router = APIRouter()

account_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
account_router.include_router(registration_router, prefix="/register", tags=["Registration"])
