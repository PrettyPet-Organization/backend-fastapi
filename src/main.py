import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config.db import db_settings
from core.routing import router as core_router
from core.config.logging import LOGGING_CONFIG, logger

# Базовая настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

app = FastAPI(debug=db_settings.echo, title="PrettyPet API")
app.include_router(core_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Application started successfully")
logger.info(f"Debug mode: {db_settings.echo}")
logger.info("CORS middleware configured for all origins")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server directly from main.py")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=db_settings.echo,
        log_config=LOGGING_CONFIG
    )
