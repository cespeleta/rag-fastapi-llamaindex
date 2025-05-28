"""Configuration class definition."""

from importlib.metadata import version as package_version
from logging import getLogger
from typing import Self

import yaml
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.config.api import ApiConfig
from app.core.config.logging import LoggingConfig
from app.core.config.rag import RagServiceConfig

logger = getLogger(__name__)


class Configuration(BaseSettings):
    """Application configuration settings."""

    app_name: str = Field()
    environment: str = Field(
        "local",
        description="Working environment.",
    )

    api: ApiConfig = Field(
        default_factory=ApiConfig.model_construct,
        title="API configuration",
        description=(
            "API configurable constants for API title, description OpenAPI endpoint "
            "and base URL."
        ),
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig.model_construct,
        title="Logging configuration",
        description=(
            "Python logger configuration options, following logging configuration "
            "dictionary schema."
        ),
    )
    rag_service: RagServiceConfig = Field(
        default_factory=RagServiceConfig.model_construct,
        title="Rag Service configuration",
    )
    hf_token: SecretStr | None = Field(
        None, description="Hugging Face API token for private models."
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def from_yaml(cls, yaml_file_path: str = "config-local.yaml") -> "Configuration":
        """Loads configuration from a YAML file."""
        with open(yaml_file_path) as f:  # noqa: PTH123
            yaml_config = yaml.safe_load(f)

        return cls(**yaml_config)

    @property
    def version(self: Self) -> str:
        """Get app package version."""
        return package_version("rag_fastapi_app")
