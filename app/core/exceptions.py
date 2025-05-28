"""API custom exceptions definitions."""


class RAGException(Exception):
    """Base exception class for the RAG service."""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)


class RAGServiceNotInitializedError(RAGException):
    """Raised when the RAG service is accessed before it is initialized."""

    pass


class QueryExecutionError(RAGException):
    """Raised when an error occurs during the RAG query execution."""

    pass


class IndexingError(RAGException):
    """Raised when an error occurs during document indexing."""

    pass


class FileUploadError(RAGException):
    """Raise when an error occurs during file upload."""

    pass
