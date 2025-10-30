import logging
import sys
from logging.config import dictConfig
from typing import Dict, Any

from core.config.main import BASE_DIR

# Logs directory
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logging_config(environment: str = "development") -> Dict[str, Any]:
    """Logging configuration based on environment."""

    base_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(levelname)-8s | %(name)s | %(message)s",
            },
            "json": {
                "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s", "filename": "%(filename)s", "funcName": "%(funcName)s", "lineno": "%(lineno)d"}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "simple",
            },
            "file_app": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "app.log",
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5,
                "formatter": "verbose",
                "encoding": "utf-8",
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "error.log",
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "formatter": "verbose",
                "level": "ERROR",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            # Root logger
            "": {
                "handlers": ["console"],
                "level": "INFO",
            },
            # Application logger
            "app": {
                "handlers": ["console", "file_app", "file_error"],
                "level": "DEBUG",
                "propagate": False,
            },
            # FastAPI loggers
            "uvicorn": {
                "handlers": ["console", "file_app"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console", "file_error"],
                "level": "ERROR",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console", "file_app"],
                "level": "INFO",
                "propagate": False,
            },
            # SQLAlchemy loggers
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            # Alembic logger
            "alembic": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    # Production environment settings
    if environment == "production":
        base_config["loggers"][""]["level"] = "WARNING"
        base_config["loggers"]["app"]["level"] = "INFO"
        base_config["loggers"]["uvicorn"]["level"] = "INFO"
        base_config["handlers"]["console"]["formatter"] = "verbose"

    # Development environment settings
    elif environment == "development":
        base_config["loggers"]["sqlalchemy.engine"]["level"] = "INFO"
        base_config["handlers"]["console"]["formatter"] = "verbose"

    return base_config


def setup_logging(environment: str = "development"):
    """Initialize logging system."""
    config = get_logging_config(environment)
    dictConfig(config)

    # Create main application logger
    logger = logging.getLogger("app")

    # Log initialization
    logger.info("Logging system initialized for %s environment", environment)
    logger.info("Logs directory: %s", LOGS_DIR.absolute())

    return logger


# Global logger instance
logger = setup_logging()