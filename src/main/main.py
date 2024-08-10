import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.presentation.api.routers import api_router
from src.main.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

logging.info("App was created.")

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)


if __name__ == "__main__":
    uvicorn.run(
        "src.main.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD
    )
