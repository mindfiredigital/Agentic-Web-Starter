from typing import Optional

from langchain_qdrant import QdrantVectorStore

from app.config.log_config import logger
from app.constants.app_constants import VECTOR_DB
from app.exceptions import InternalError
from app.repository.vector_repository import qdrant_repository


class VectorRetriever:
    """Qdrant-backed retriever for existing collections."""

    def __init__(self, collection_name: Optional[str] = None):
        self.qdrant_repo = qdrant_repository
        self.collection_name = collection_name or self.qdrant_repo.get_collection_name_with_model()
        self.vectordb: Optional[QdrantVectorStore] = None
        self.top_k = VECTOR_DB.TOP_K.value

    def initialize_vectordb(self) -> QdrantVectorStore:
        """Connect to an existing Qdrant collection.

        Returns:
            Initialized Qdrant vector store.
        """
        self.vectordb = self.qdrant_repo.build_vectordb(collection_name=self.collection_name)

        return self.vectordb

    def search(self, query: str):
        """Return top-k documents matching the query.

        Args:
            query: Search query string.

        Returns:
            List of matching documents.
        """
        if not query:
            logger.warning("Empty query provided; returning no results")
            return []

        if self.vectordb is None:
            self.initialize_vectordb()

        try:
            return self.vectordb.similarity_search(query, k=self.top_k)
        except Exception as e:
            logger.exception("Error querying qdrant vectordb: %s", e)
            raise InternalError("Retrieval failed") from e

