"""API main app definition."""

from fastapi import FastAPI

from app.api.error_handlers import add_exception_handlers
from app.api.health import router as health_router
from app.api.lifespan import lifespan
from app.api.middlewares import add_middlewares
from app.api.v1.router import router as v1_router
from app.core.config.configuration import Configuration


def build_service_app() -> FastAPI:
    """Build service FastAPI app."""
    config = Configuration.from_yaml()
    app = FastAPI(
        title=config.api.title,
        description=config.api.description,
        openapi_url=config.api.openapi_url,
        version=config.version,
        lifespan=lifespan,
    )
    app.include_router(router=health_router)
    app.include_router(router=v1_router, prefix=config.api.prefix)
    add_exception_handlers(app=app)
    add_middlewares(app=app, config=config)
    return app
