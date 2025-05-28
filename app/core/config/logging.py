"""Logging configuration class definition."""

from pydantic import BaseModel


class LoggingConfig(BaseModel):
    """Logging configuration model, to be used through logging.config.dictConfig."""

    version: int = 1
    disable_existing_loggers: bool = False
    incremental: bool = False
    formatters: dict[str, dict] | None = None
    filters: dict[str, dict] | None = None
    handlers: dict[str, dict] | None = None
    loggers: dict[str, dict] | None = None
    root: dict | None = None
