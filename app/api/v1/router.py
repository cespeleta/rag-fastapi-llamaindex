"""API router definition."""

from fastapi import APIRouter

from app.api.v1.routes import rag

router = APIRouter()
router.include_router(router=rag.router, prefix="/query", tags=["RAG"])
