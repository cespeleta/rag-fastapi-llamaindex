from unittest.mock import Mock, patch

import pytest

from app.services.components.vector_store import ChromaVectorStoreComponent


class TestChromaVectorStoreComponent:
    """Test cases for ChromaVectorStoreComponent class."""

    def test_initialization(self, mock_rag_config_vector_store: Mock) -> None:
        """Test that the component initializes correctly with configuration."""
        component = ChromaVectorStoreComponent(mock_rag_config_vector_store)

        assert component._config == mock_rag_config_vector_store
        assert component._store is None
        assert component._client is None

    def test_get_store_success(self, mock_rag_config_vector_store: Mock) -> None:
        """Test successful retrieval of loaded vector store."""
        mock_chroma_vector_store = Mock()
        component = ChromaVectorStoreComponent(mock_rag_config_vector_store)
        component._store = mock_chroma_vector_store

        result = component.get_store()

        assert result == mock_chroma_vector_store

    def test_get_store_not_loaded_raises_error(
        self, mock_rag_config_vector_store: Mock
    ) -> None:
        """Test that get_store raises ValueError when store is not loaded."""
        component = ChromaVectorStoreComponent(mock_rag_config_vector_store)

        with pytest.raises(
            ValueError, match="Vector Store has not been loaded. Call load\\(\\) first."
        ):
            component.get_store()

    def test_clear_collections_client_not_initialized_raises_error(
        self, mock_rag_config_vector_store: Mock
    ) -> None:
        """Test that clear_collections raises ValueError when client is not initialized."""
        component = ChromaVectorStoreComponent(mock_rag_config_vector_store)

        with pytest.raises(ValueError, match="ChromaDB client is not initialized."):
            component.clear_collections()

    @patch("app.services.components.vector_store.logger")
    def test_shutdown(
        self, mock_logger: Mock, mock_rag_config_vector_store: Mock
    ) -> None:
        """Test shutdown functionality releases resources from memory."""
        component = ChromaVectorStoreComponent(mock_rag_config_vector_store)
        component._store = Mock()
        component._client = Mock()

        component.shutdown()

        # Verify resources were cleared
        assert component._store is None
        assert component._client is None

        # Verify logging message
        mock_logger.info.assert_called_once_with(
            "Shutting down vector store component."
        )
