"""HuggingFace LLM class definition."""

from logging import getLogger
from typing import Any

from llama_index.core.llms import LLM
from llama_index.llms.huggingface import HuggingFaceLLM

from app.core.config.rag import RagServiceConfig

logger = getLogger(__name__)


class HuggingFaceLLMComponent:
    """Manages the HuggingFace Language Model."""

    def __init__(self, config: RagServiceConfig):
        """Initizalizes the component with configuration."""
        self._config = config
        self._model: LLM | None = None

    def load(self) -> None:
        """Loads the LLM model into memory."""
        logger.info(f"Loading LLM model: {self._config.llm_model_name}")
        llm_kwargs: dict[str, Any] = {
            "model_name": self._config.llm_model_name,
            "tokenizer_name": self._config.llm_model_name,
            "context_window": self._config.context_window,
            "max_new_tokens": self._config.max_new_tokens,
            "generate_kwargs": {
                "temperature": self._config.temperature,
                "do_sample": True,
            },
            "device_map": self._config.device_map,
        }

        self._model = HuggingFaceLLM(**llm_kwargs)
        logger.info("LLM model loaded sucessfully.")

    def get_model(self) -> LLM:
        """Returns the loaded LLM model."""
        if not self._model:
            raise ValueError("LLM model has not been loaded. Call load() first.")
        return self._model

    def shutdown(self) -> None:
        """Releases the model from memory."""
        logger.info("Shutting down LLM model component.")
        self._model = None
