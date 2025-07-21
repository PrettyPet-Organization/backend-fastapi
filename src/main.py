import asyncio

from fastapi import FastAPI

from core.config import settings_config
from core.routing import router as core_router


app = FastAPI(debug=settings_config.debug, title="PrettyPet API")
app.include_router(core_router)


# I'm not sure if we need this block.
async def main() -> None:
    import uvicorn

    from core.config import LOGGING_CONFIG

    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        reload=settings_config.debug,
        log_config=LOGGING_CONFIG,
    )


if __name__ == "__main__":
    asyncio.run(main())
