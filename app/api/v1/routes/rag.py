"""API v2 RAG routes definitions."""

from logging import getLogger

from fastapi import APIRouter, Body, Depends, status

from app.api.dependencies import get_rag_service
from app.api.v1.schemas import (
    RAGErrorResponse,
    RAGQueryRequest,
    RAGQueryResponse,
)
from app.services.rag_service import RAGService

logger = getLogger(__name__)
router = APIRouter()


@router.post(
    "/query",
    response_model=RAGQueryResponse | RAGErrorResponse,
    summary="Query the RAG system",
    description="Send a prompt to the RAG system and get an answer \
        based on indexed PDF documents.",
    responses={
        status.HTTP_200_OK: {"model": RAGQueryResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": RAGErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": RAGErrorResponse},
    },
)
async def query_rag(
    request: RAGQueryRequest = Body(...),
    rag_service: RAGService = Depends(get_rag_service),
):
    """Endpoint to submit a query to the RAG system."""

    result = await rag_service.query(prompt=request.prompt)
    return RAGQueryResponse(**result)
