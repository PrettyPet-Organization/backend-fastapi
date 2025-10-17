import logging
from logging.config import dictConfig
from pathlib import Path

from core.config.main import BASE_DIR

LOGS_DIR = BASE_DIR / "logs"

# Create a directory if it doesn't exist
Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "json": {
            "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", '
            '"level": "%(levelname)s", "message": "%(message)s"}'
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"},
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "app.log",
            "formatter": "json",
        },
    },
    "loggers": {
        "dev": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": False},
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "WARNING",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("dev")
