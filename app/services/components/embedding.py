"""Embeddings class definition."""

from logging import getLogger

from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from app.core.config.rag import RagServiceConfig

logger = getLogger(__name__)


class HuggingFaceEmbeddingComponent:
    """Manages the HuggingFace embedding model."""

    def __init__(self, config: RagServiceConfig):
        """Initizalizes the component with configuration."""
        self._config = config
        self._model: BaseEmbedding | None = None

    def load(self) -> None:
        """Loads the embedding model into memory."""
        logger.info(f"Loading embedding model: {self._config.embed_model_name}")
        self._model = HuggingFaceEmbedding(model_name=self._config.embed_model_name)
        logger.info("Embedding model loaded sucessfully.")

    def get_model(self) -> BaseEmbedding:
        """Returns the loaded embedding model."""
        if not self._model:
            raise ValueError("Embedding model has not been loaded. Call load() first.")
        return self._model

    def shutdown(self) -> None:
        """Releases the model from memory."""
        logger.info("Shutting down embedding model component.")
        self._model = None
