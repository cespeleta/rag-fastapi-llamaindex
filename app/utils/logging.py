"""Logging utilities."""

from logging.config import dictConfig

from app.core.config.logging import LoggingConfig


def configure_logging(logging_config: LoggingConfig):
    """Configure logging from configuration."""
    dict_config = logging_config.model_dump(exclude_none=True)
    dictConfig(dict_config)
