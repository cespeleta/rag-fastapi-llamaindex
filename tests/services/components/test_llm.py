"""Unit tests for HuggingFaceLLMComponent class."""

from unittest.mock import Mock, patch

import pytest

from app.services.components.llm import HuggingFaceLLMComponent


class TestHuggingFaceLLMComponent:
    """Test cases for HuggingFaceLLMComponent class."""

    def test_initialization(self, mock_rag_config_llm: Mock) -> None:
        """Test that the component initializes correctly with configuration.

        Args:
            mock_rag_config_llm: Mock configuration object with LLM settings.
        """
        component = HuggingFaceLLMComponent(mock_rag_config_llm)

        assert component._config == mock_rag_config_llm
        assert component._model is None

    @patch("app.services.components.llm.HuggingFaceLLM")
    @patch("app.services.components.llm.logger")
    def test_load_model_success(
        self,
        mock_logger: Mock,
        mock_huggingface_llm_class: Mock,
        mock_rag_config_llm: Mock,
        mock_huggingface_llm: Mock,
    ) -> None:
        """Test successful loading of the LLM model with correct parameters."""
        mock_huggingface_llm_class.return_value = mock_huggingface_llm
        component = HuggingFaceLLMComponent(mock_rag_config_llm)

        component.load()

        # Verify model was created with correct parameters
        expected_kwargs = {
            "model_name": mock_rag_config_llm.llm_model_name,
            "tokenizer_name": mock_rag_config_llm.llm_model_name,
            "context_window": mock_rag_config_llm.context_window,
            "max_new_tokens": mock_rag_config_llm.max_new_tokens,
            "generate_kwargs": {
                "temperature": mock_rag_config_llm.temperature,
                "do_sample": True,
            },
            "device_map": mock_rag_config_llm.device_map,
        }
        mock_huggingface_llm_class.assert_called_once_with(**expected_kwargs)

        # Verify model was stored
        assert component._model == mock_huggingface_llm

        # Verify logging messages
        assert mock_logger.info.call_count == 2
        mock_logger.info.assert_any_call(
            f"Loading LLM model: {mock_rag_config_llm.llm_model_name}"
        )
        mock_logger.info.assert_any_call("LLM model loaded sucessfully.")

    def test_get_model_success(
        self, mock_rag_config_llm: Mock, mock_huggingface_llm: Mock
    ) -> None:
        """Test successful retrieval of loaded LLM model."""
        component = HuggingFaceLLMComponent(mock_rag_config_llm)
        component._model = mock_huggingface_llm

        result = component.get_model()

        assert result == mock_huggingface_llm
        assert isinstance(result, type(mock_huggingface_llm))

    def test_get_model_not_loaded_raises_error(self, mock_rag_config_llm: Mock) -> None:
        """Test that get_model raises ValueError when model is not loaded."""
        component = HuggingFaceLLMComponent(mock_rag_config_llm)

        with pytest.raises(
            ValueError, match="LLM model has not been loaded. Call load\\(\\) first."
        ):
            component.get_model()

    @patch("app.services.components.llm.logger")
    def test_shutdown(self, mock_logger: Mock, mock_rag_config_llm: Mock) -> None:
        """Test shutdown functionality releases model from memory."""
        component = HuggingFaceLLMComponent(mock_rag_config_llm)
        component._model = Mock()  # Simulate loaded model

        component.shutdown()

        # Verify model was cleared
        assert component._model is None

        # Verify logging message
        mock_logger.info.assert_called_once_with("Shutting down LLM model component.")
