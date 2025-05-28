"""API middleware app definition."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.configuration import Configuration


def add_cors_middleware(app: FastAPI, config: Configuration) -> None:
    """
    Add CORS middleware to the FastAPI application.

    This allows the frontend development server to make requests to the API.
    """
    if config.environment == "local":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def add_middlewares(app: FastAPI, config: Configuration):
    """Add middlewares to the FastAPI application."""
    add_cors_middleware(app, config)
