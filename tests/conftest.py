"""Shared fixtures for embedding component tests."""

from unittest.mock import Mock

import pytest

from app.core.config.rag import RagServiceConfig


@pytest.fixture
def mock_rag_config() -> Mock:
    """Create a mock RagServiceConfig for testing.

    Returns:
        Mock: A mock configuration object with embed_model_name attribute.
    """
    config = Mock(spec=RagServiceConfig)
    config.embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return config


@pytest.fixture
def mock_huggingface_embedding() -> Mock:
    """Create a mock HuggingFaceEmbedding instance.

    Returns:
        Mock: A mock embedding model instance.
    """
    mock_embedding = Mock()
    mock_embedding.model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return mock_embedding


@pytest.fixture
def mock_rag_config_llm() -> Mock:
    """Create a mock RagServiceConfig for LLM testing.

    Returns:
        Mock: A mock configuration object with LLM-specific attributes.
    """
    config = Mock(spec=RagServiceConfig)
    config.llm_model_name = "microsoft/DialoGPT-medium"
    config.context_window = 2048
    config.max_new_tokens = 512
    config.temperature = 0.7
    config.device_map = "auto"
    return config


@pytest.fixture
def mock_huggingface_llm() -> Mock:
    """Create a mock HuggingFaceLLM instance.

    Returns:
        Mock: A mock LLM model instance.
    """
    mock_llm = Mock()
    mock_llm.model_name = "microsoft/DialoGPT-medium"
    return mock_llm


@pytest.fixture
def mock_rag_config_vector_store() -> Mock:
    """Create a mock RagServiceConfig for vector store testing.

    Returns:
        Mock: A mock configuration object with vector store-specific attributes.
    """
    from pathlib import Path

    config = Mock(spec=RagServiceConfig)
    config.vector_store_path = Path("./test_vector_store")
    config.collection_name = "test_collection"
    return config
