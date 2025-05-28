"""Main module entrypoint definition."""

from logging import getLogger

from app.core.config.configuration import Configuration
from app.utils.logging import configure_logging

logger = getLogger(__name__)


def main():
    """Main entrypoint."""
    config = Configuration.from_yaml("config-local.yaml")
    configure_logging(logging_config=config.logging)
    logger.info(
        "Service name: %s. Version: %s",
        config.app_name,
        config.version,
    )
    logger.info(config)
