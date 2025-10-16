from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config.db import get_db

router = APIRouter()


@router.get("")
async def health_check(db: Session = Depends(get_db)) -> dict:
    """Service health check endpoint with database connectivity."""
    try:
        start_time = datetime.now()
        db.execute(text("SELECT 1"))
        db_connection_time = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "status": "healthy",
            "service": "backend-fastapi",
            "timestamp": datetime.now().isoformat(),
            "database": {
                "status": "connected",
                "connection_time_ms": round(db_connection_time, 2),
            },
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "backend-fastapi",
            "timestamp": datetime.now().isoformat(),
            "database": {"status": "disconnected", "error": str(e)},
        }
