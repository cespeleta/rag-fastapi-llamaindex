"""API error handler definitions."""

from logging import getLogger

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    IndexingError,
    QueryExecutionError,
    RAGException,
    RAGServiceNotInitializedError,
)

logger = getLogger(__name__)


def rag_exception_handler(request: Request, exc: RAGException) -> JSONResponse:  # noqa: ARG001
    """Generic handler for RAG-related exceptions."""
    logger.error(f"A RAG-related error ocurred: {exc.detail}", exc_info=True)
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Assign specific status codes for specific errors
    if isinstance(exc, RAGServiceNotInitializedError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    if isinstance(exc, QueryExecutionError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, IndexingError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(
        status_code=status_code,
        content={"error": exc.__class__.__name__, "detail": exc.detail},
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Adds all custom exception handlers to the FastAPI app."""
    app.add_exception_handler(RAGException, rag_exception_handler)  # type: ignore
