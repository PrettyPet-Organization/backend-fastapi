from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def health_check() -> dict[str, str]:
    """Service health check endpoint."""
    return {"status": "ok"}
