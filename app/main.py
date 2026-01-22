from fastapi import FastAPI
from app.api.routers import router


def get_application() -> FastAPI:
    application = FastAPI(
        title="Organisations API",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    application.include_router(router)
    return application
