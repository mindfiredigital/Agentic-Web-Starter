from typing import List, Optional

from langchain_qdrant import QdrantVectorStore

from app.config.log_config import logger
from app.repository.vector_repository.qdrant_repository import qdrant_repository


class Indexer:
    """Qdrant-backed indexer for embedding chunks."""

    def __init__(self) -> None:
        """Initialize indexer with Qdrant repository and collection name."""
        self.qdrant_repo = qdrant_repository
        self.collection_name = self.qdrant_repo.get_collection_name_with_model()
        self.vectordb: Optional[QdrantVectorStore] = None

    def initialize_vectordb(self) -> QdrantVectorStore:
        """Initialize Qdrant collection and return vector store.

        Returns:
            Initialized QdrantVectorStore instance.
        """
        self.vectordb = self.qdrant_repo.build_vectordb(
            collection_name=self.collection_name
        )
        return self.vectordb

    def index_documents(self, chunks: List):
        """Add chunks to Qdrant (initialize if needed).

        Args:
            chunks: List of document chunks to index.

        Returns:
            Dict with success status and collection_name, or None if no chunks.

        Raises:
            ValueError: If indexing fails.
        """
        if not chunks:
            logger.warning("No chunks provided; skipping indexing")
            return

        if self.vectordb is None:
            self.initialize_vectordb()

        store = self.initialize_vectordb() if self.vectordb is None else self.vectordb

        try:
            store.add_documents(chunks)
            logger.info("Documents added to qdrant vectordb successfully")
            return {"success": True, "collection_name": self.collection_name}
        except Exception as e:
            logger.error("Error adding documents to qdrant vectordb: %s", e)
            raise ValueError(
                f"Error adding documents to qdrant vectordb: {str(e)}"
            ) from e

    def delete_database(self):
        """Delete the vector database.

        Returns:
            Dict with success status and collection_name, or None if collection absent.

        Raises:
            ValueError: If deletion fails.
        """
        if not self.qdrant_repo.collection_exists(self.collection_name):
            logger.warning(
                "Collection %s not found; skipping deletion", self.collection_name
            )
            return

        try:
            self.qdrant_repo.delete_collection(collection_name=self.collection_name)
            logger.info("Vector database deleted successfully")
            return {"success": True, "collection_name": self.collection_name}
        except Exception as e:
            logger.error("Error deleting vector database: %s", e)
            raise ValueError(f"Error deleting vector database: {str(e)}") from e
