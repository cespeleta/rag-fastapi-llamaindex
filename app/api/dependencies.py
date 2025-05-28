"""API dependency function definitions."""

from fastapi import Request

from app.core.exceptions import RAGServiceNotInitializedError
from app.services.rag_service import (
    RAGService,
)


def get_rag_service(request: Request) -> RAGService:
    """Get RAGService from the application state."""
    rag_service = getattr(request.app.state, "rag_service", None)
    if rag_service is None:
        raise RAGServiceNotInitializedError(
            "RAGService not initialized. Check application startup."
        )
    return rag_service
