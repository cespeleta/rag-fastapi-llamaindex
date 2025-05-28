"""Unit tests for HuggingFaceEmbeddingComponent class."""

from unittest.mock import Mock, patch

import pytest

from app.services.components.embedding import HuggingFaceEmbeddingComponent


class TestHuggingFaceEmbeddingComponent:
    """Test cases for HuggingFaceEmbeddingComponent class."""

    def test_initialization(self, mock_rag_config: Mock) -> None:
        """Test that the component initializes correctly with configuration.

        Args:
            mock_rag_config: Mock configuration object.
        """
        component = HuggingFaceEmbeddingComponent(mock_rag_config)

        assert component._config == mock_rag_config
        assert component._model is None

    @patch("app.services.components.embedding.HuggingFaceEmbedding")
    @patch("app.services.components.embedding.logger")
    def test_load_model_success(
        self,
        mock_logger: Mock,
        mock_huggingface_class: Mock,
        mock_rag_config: Mock,
        mock_huggingface_embedding: Mock,
    ) -> None:
        """Test successful loading of the embedding model."""
        mock_huggingface_class.return_value = mock_huggingface_embedding
        component = HuggingFaceEmbeddingComponent(mock_rag_config)

        component.load()

        # Verify model was created with correct parameters
        mock_huggingface_class.assert_called_once_with(
            model_name=mock_rag_config.embed_model_name
        )

        # Verify model was stored
        assert component._model == mock_huggingface_embedding

        # Verify logging messages
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call(
            f"Loading embedding model: {mock_rag_config.embed_model_name}"
        )
        mock_logger.info.assert_any_call("Embedding model loaded sucessfully.")

    def test_get_model_success(
        self, mock_rag_config: Mock, mock_huggingface_embedding: Mock
    ) -> None:
        """Test successful retrieval of loaded embedding model."""
        component = HuggingFaceEmbeddingComponent(mock_rag_config)
        component._model = mock_huggingface_embedding

        result = component.get_model()

        assert result == mock_huggingface_embedding
        assert isinstance(result, type(mock_huggingface_embedding))

    def test_get_model_not_loaded_raises_error(self, mock_rag_config: Mock) -> None:
        """Test that get_model raises ValueError when model is not loaded."""
        component = HuggingFaceEmbeddingComponent(mock_rag_config)

        with pytest.raises(
            ValueError,
            match="Embedding model has not been loaded. Call load\\(\\) first.",
        ):
            component.get_model()

    @patch("app.services.components.embedding.logger")
    def test_shutdown(self, mock_logger: Mock, mock_rag_config: Mock) -> None:
        """Test shutdown functionality releases model from memory."""
        component = HuggingFaceEmbeddingComponent(mock_rag_config)
        component._model = Mock()  # Simulate loaded model

        component.shutdown()

        # Verify model was cleared
        assert component._model is None

        # Verify logging message
        mock_logger.info.assert_called_once_with(
            "Shutting down embedding model component."
        )
