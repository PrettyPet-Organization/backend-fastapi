import asyncio

from fastapi import FastAPI

from core.config import settings
from core.routing import router as core_router


app = FastAPI(debug=settings.debug, title="PrettyPet API")
app.include_router(core_router)


async def main() -> None:
    import uvicorn

    from core.config import LOGGING_CONFIG

    uvicorn.run(
        "main:app", host="0.0.0.0", reload=settings.debug, log_config=LOGGING_CONFIG
    )


if __name__ == "__main__":
    asyncio.run(main())
