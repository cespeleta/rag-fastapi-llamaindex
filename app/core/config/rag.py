"""API configuration class definition."""

from pathlib import Path

from pydantic import BaseModel, Field


class RagServiceConfig(BaseModel):
    """RAG Config configuration model."""

    pdf_directory: str = Field(
        "./data",
        description="Directory for PDF files",
    )
    vector_store_path: Path = Field(
        Path("./vector_store"),
        description="Path for ChromaDB persistence",
    )
    collection_name: str = Field(
        "rag_documents",
        description="ChromaDB collection name",
    )
    embed_model_name: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model name",
    )
    llm_model_name: str = Field(
        "NousResearch/Llama-2-7b-chat-hf",
        description="LLM model name",
    )
    temperature: float = Field(0.1, ge=0.0, le=1.0, description="LLM temperature")
    max_new_tokens: int = Field(512, gt=0, description="LLM max new tokens")
    context_window: int = Field(4096, gt=0, description="LLM context window size")
    device_map: str | None = Field(
        "auto", description="Device map for HugginfFace models ('auto', 'cpu', 'cuda')"
    )
    template_dir: Path = Field(
        Path("app/templates"),
        description="Directory for prompt templates.",
    )
    template_file: str = Field(
        "qa_template.jinja2",
        description="Filename for the prompt template.",
    )
