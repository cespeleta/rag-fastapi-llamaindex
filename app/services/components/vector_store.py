"""ChromaDB class definition."""

from logging import getLogger
from pathlib import Path

from llama_index.vector_stores.chroma import ChromaVectorStore

import chromadb
from app.core.config.rag import RagServiceConfig
from chromadb.api import ClientAPI
from chromadb.config import Settings

logger = getLogger(__name__)


class ChromaVectorStoreComponent:
    """Manages the ChromaDB Vector Store."""

    def __init__(self, config: RagServiceConfig):
        """Initizalizes the component with configuration."""
        self._config = config
        self._store: ChromaVectorStore | None = None
        self._client: ClientAPI | None = None

    def load(self) -> None:
        """Loads the ChromaDB client and gets the vector store."""
        logger.info(
            f"Initializing ChromaDB at path: {self._config.vector_store_path} "
            f"with collection: {self._config.collection_name}"
        )
        Path.mkdir(self._config.vector_store_path, exist_ok=True, parents=True)
        self._client = chromadb.PersistentClient(
            path=str(self._config.vector_store_path),
            settings=Settings(anonymized_telemetry=False),
        )
        chroma_collection = self._client.get_or_create_collection(
            self._config.collection_name,
            metadata={
                "hnsw:space": "l2",  # Euclidean Distance Squared
                "hnsw:batch_size": 100,  # Default
            },
        )
        self._store = ChromaVectorStore(chroma_collection=chroma_collection)
        logger.info("ChromaDB vector store initialized successfully.")

    def get_store(self) -> ChromaVectorStore:
        """Returns the initialized vector store."""
        if not self._store:
            raise ValueError("Vector Store has not been loaded. Call load() first.")
        return self._store

    def clear_collections(self) -> None:
        """Deletes and recreates the collection, clearing all data."""
        if not self._client:
            raise ValueError("ChromaDB client is not initialized.")

        collection_name = self._config.collection_name
        logger.info(f"Clearing vector store collection: {collection_name}")
        self._client.delete_collection(name=collection_name)
        new_collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={
                "hnsw:space": "l2",  # Euclidean Distance Squared
                "hnsw:batch_size": 100,  # Default
            },
        )
        self._store = ChromaVectorStore(chroma_collection=new_collection)
        logger.info(f"Collection '{collection_name}' cleared and recreated.")

    def shutdown(self) -> None:
        """Shuts down the vector store component."""
        logger.info("Shutting down vector store component.")
        self._store = None
        self._client = None
