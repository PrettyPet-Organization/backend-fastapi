import os
import sys
from datetime import datetime

import psutil
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.config.db import get_db

router = APIRouter()


@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """Service health check endpoint with database connectivity."""
    health_status = {
        "status": "healthy",
        "service": "backend-fastapi",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "dependencies": {},
        "system": {}
    }

    # 1. Проверка базы данных через асинхронную сессию
    try:
        start_time = datetime.now()
        result = await db.scalars(text("SELECT 1"))
        test_value = result.first()
        db_connection_time = (datetime.now() - start_time).total_seconds() * 1000

        health_status["dependencies"]["database"] = {
            "status": "connected",
            "connection_time_ms": round(db_connection_time, 2),
            "type": "PostgreSQL",
            "driver": "asyncpg"  # теперь используем asyncpg через SQLAlchemy
        }

        if test_value != 1:
            health_status["status"] = "unhealthy"

    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["dependencies"]["database"] = {
            "status": "disconnected",
            "error": str(e)
        }

    # 2. Системная информация
    health_status["system"] = {
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }

    # 3. Информация о приложении
    health_status["dependencies"]["api"] = {
        "status": "healthy",
        "framework": "FastAPI"
    }

    return health_status
