import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings_config
from core.routing import router as core_router


app = FastAPI(debug=settings_config.debug, title="PrettyPet API")
app.include_router(core_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
