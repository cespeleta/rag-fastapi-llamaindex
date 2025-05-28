"""API lifespan definition."""

from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.core.config.configuration import Configuration
from app.services.rag_service import initialize_rag_service
from app.utils.logging import configure_logging

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event(app)
    yield
    await shutdown_event(app)


async def startup_event(app: FastAPI):
    """Lifespan function handling API startup and teardown logic."""
    logger.info("Application startup: API is starting up")
    config = Configuration.from_yaml()
    configure_logging(logging_config=config.logging)
    logger.info(
        "App name: %s. Version: %s",
        config.app_name,
        config.version,
    )
    app.state.rag_service = await initialize_rag_service(config.rag_service)


async def shutdown_event(app: FastAPI):
    """Lifespan function handling API shutdown logic."""
    logger.info("Application shutdown: Cleaning up RAG service...")
    if rag_service := getattr(app.state, "rag_service", None):
        try:
            await rag_service.shutdown()
            logger.info("RAG service shutdown complete.")
        except Exception as e:
            logger.error(f"Error during RAG service shutdown: {e}")
