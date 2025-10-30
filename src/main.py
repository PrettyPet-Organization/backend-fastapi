from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.config.db import db_settings
from core.config.logging import logger, setup_logging
from core.config.settings import settings

# Initialize logging based on environment
setup_logging(settings.ENVIRONMENT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown events.
    Handles initialization and cleanup of resources.
    """
    # Startup logic
    logger.info("Starting PrettyPet API application")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {db_settings.echo}")

    try:
        # Initialize database connections and other resources here
        logger.info("Initializing application resources...")
        yield

    except Exception as e:
        logger.error(f"Error during application startup: {e}")
        raise

    finally:
        # Shutdown logic
        logger.info("Shutting down PrettyPet API application")
        # Cleanup resources here


def create_application() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    Centralizes all application configuration and setup.
    """
    application = FastAPI(
        debug=db_settings.echo,
        title="PrettyPet API",
        description="API for PrettyPet platform - User management and projects",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Configure CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Consider restricting in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request logging middleware
    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        """
        Middleware to log all incoming requests and responses.
        Provides visibility into API usage and performance.
        """
        logger.info(f"Incoming request: {request.method} {request.url}")

        try:
            response = await call_next(request)
            logger.info(f"Response: {request.method} {request.url} - Status: {response.status_code}")
            return response

        except Exception as e:
            logger.error(f"Unhandled exception in request: {e}")
            raise

    # Global exception handlers
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Global handler for Pydantic validation errors.
        Provides consistent error responses for invalid requests.
        """
        logger.warning(f"Validation error for {request.method} {request.url}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Global handler for unhandled exceptions.
        Prevents sensitive error details from leaking to clients.
        """
        logger.error(f"Unhandled exception for {request.method} {request.url}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    # Register all application routers
    register_routers(application)

    return application


def register_routers(app: FastAPI):
    """
    Register all API routers with the application.
    Centralized router registration for better maintainability.
    """
    try:
        from core.routing import core_router
        app.include_router(core_router, prefix="/api/v1")
        logger.info("Core routes registered successfully")
    except ImportError as e:
        logger.error(f"Failed to register core routes: {e}")

    try:
        from account.routing import account_router
        app.include_router(account_router, prefix="/api/v1")
        logger.info("Account routes registered successfully")
    except ImportError as e:
        logger.error(f"Failed to register account routes: {e}")


# Create the application instance
app = create_application()


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    Serves as a welcome and discovery endpoint.
    """
    return {
        "message": "PrettyPet API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    Provides basic service status information.
    """
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "PrettyPet API",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn

    """
    Entry point for running the application directly.
    Used for development purposes with auto-reload.
    """
    logger.info("Starting uvicorn server directly from main.py")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=db_settings.echo,
        log_level="info",
        access_log=True,
    )