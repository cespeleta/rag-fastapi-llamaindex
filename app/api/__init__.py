"""API configuration package entrypoint."""

from app.api.main import build_service_app

__all__ = [
    "build_service_app",
]
