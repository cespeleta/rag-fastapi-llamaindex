"""RAG Service class definition."""

from logging import getLogger
from pathlib import Path
from typing import Any

from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.prompts import RichPromptTemplate

from app.core.config.rag import RagServiceConfig
from app.core.exceptions import IndexingError, QueryExecutionError
from app.services.components import (
    ChromaVectorStoreComponent,
    HuggingFaceEmbeddingComponent,
    HuggingFaceLLMComponent,
)

logger = getLogger(__name__)


class RAGService:
    """Service class for handling Retrieval Augmented Generation (RAG) operations."""

    def __init__(
        self,
        llm_component: HuggingFaceLLMComponent,
        embedding_component: HuggingFaceEmbeddingComponent,
        vector_store_component: ChromaVectorStoreComponent,
        config: RagServiceConfig,
    ):
        """Initializes the RAGService."""
        self._llm_component = llm_component
        self._embedding_component = embedding_component
        self._vector_store_component = vector_store_component
        self._config = config
        self._index: VectorStoreIndex | None = None

        self._prompt_template: RichPromptTemplate | None = None

        # # Globally set the models for LlamaIndex
        # Settings.llm = self._llm_component.get_model()
        # Settings.embed_model = self._embedding_component.get_model()

        # Load template during initialization
        self._load_template()

    def _load_template(self):
        """Loads the prompt template from the configured file."""
        template_path = self._config.template_dir / self._config.template_file
        try:
            with Path.open(template_path) as f:
                template_str = f.read()
            self._prompt_template = RichPromptTemplate(template_str)
            logger.info(f"Successfully loaded prompt template from: {template_path}")
        except FileNotFoundError as e:
            logger.error(f"Prompt template file not found at: {template_path}")
            raise IndexingError(
                f"Could not find prompt template at {template_path}"
            ) from e

    def _load_and_index_documents(self, force_reindex: bool = False):
        """Load and index documents in the vector store."""
        vector_store = self._vector_store_component.get_store()
        collection_empty = vector_store.client.count() == 0
        if not force_reindex and not collection_empty:
            logger.info("Existing collection found. Loading index from vector store.")
            self._index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                embed_model=self._embedding_component.get_model(),
            )
            return

        if force_reindex:
            self._vector_store_component.clear_collections()

        reader = SimpleDirectoryReader(input_dir=self._config.pdf_directory)
        documents = reader.load_data()
        if not documents:
            logger.warning(
                "No PDF documents found in %s. Index will be empty.",
                self._config.pdf_directory,
            )
            # Create an empty index to avoid errors on query.
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self._index = VectorStoreIndex.from_documents(
                documents=[], storage_context=storage_context
            )
            return

        logger.info(f"Indexing {len(documents)} documents(s)...")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self._index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            embed_model=self._embedding_component.get_model(),
            show_progress=True,
        )
        logger.info("Indexing complete.")

    def get_or_create_index(self, force_reindex: bool = False):
        """Get or create a new index."""
        if self._index is None or force_reindex:
            self._load_and_index_documents(force_reindex)
        if self._index is None:
            raise IndexingError("Failed to initialize or load the document index.")

    async def query(self, prompt: str) -> dict[str, Any]:
        """Asynchronously queries the indexed documents."""
        if self._index is None:
            raise QueryExecutionError(
                "Index is not available. Please ensure documens are indexed."
            )
        if self._prompt_template is None:
            raise QueryExecutionError("Prompt template is not loaded.")

        # template = """
        # You are a professional and objective assistant.
        # Your goal is to provide answers based exclusively on the context provided.

        # Here are the rules you must follow:
        # 1. Analyze the context provided below to answer the user's question.
        # 2. If the context contains the necessary information, formulate a clear and concise answer.
        # 3. If the context does not contain the information to answer the question, you must state: "The provided context does not contain enough information to answer this question."
        # 4. You must not use any external knowledge or information you were trained on. Your resopnse must be grounded in the provided text.
        # 5. Do not make up information.

        # Context:
        # ---------------------
        # { context_str }
        # ---------------------

        # Based only on the context above, please answer the following question.

        # User's question: { query_str }

        # Answer:
        # """
        # llm_prompt = PromptTemplate(template)
        llm_prompt = self._prompt_template.format(query_str=prompt)

        logger.info(f"Executing async query: '{prompt}'")
        query_engine = self._index.as_query_engine(
            llm=self._llm_component.get_model(),
            response_mode="tree_summarize",
            text_qa_template=llm_prompt,
        )
        try:
            response = await query_engine.aquery(prompt)
        except Exception as e:
            logger.error(f"Error during query engine execution: {e}", exc_info=True)
            raise QueryExecutionError(f"Failed to execute query: {e}") from e

        source_nodes_data = [
            {
                "text": node.get_content()[:500] + "...",
                "score": float(node.get_score() if node.get_score() else 0.0),
                "node_id": node.node_id,
                "metadata": node.metadata,
            }
            for node in response.source_nodes
        ]
        logger.info(f"Generated answer: {response!s}")
        return {"answer": str(response), "sources": source_nodes_data}

    async def shutdown(self) -> None:
        """Shutdown service and components."""
        logger.info("RAG service shutdown complete.")
        self._llm_component.shutdown()
        self._embedding_component.shutdown()
        self._vector_store_component.shutdown()
        self._index = None


async def initialize_rag_service(config: RagServiceConfig) -> RAGService:
    """Creates and initializes all components and the RAG service."""
    logger.info("Initializing RAG service and its components...")
    # Initialize components
    llm_component = HuggingFaceLLMComponent(config)
    llm_component.load()
    embedding_component = HuggingFaceEmbeddingComponent(config)
    embedding_component.load()
    vector_store_component = ChromaVectorStoreComponent(config)
    vector_store_component.load()
    # Intialize service
    rag_service = RAGService(
        llm_component=llm_component,
        embedding_component=embedding_component,
        vector_store_component=vector_store_component,
        config=config,
    )
    rag_service.get_or_create_index()
    logger.info("RAGService instance initialized successfully.")
    return rag_service
