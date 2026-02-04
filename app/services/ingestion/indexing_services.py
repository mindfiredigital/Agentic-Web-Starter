from typing import List, Optional

from langchain_qdrant import QdrantVectorStore

from app.config.log_config import logger
from app.services.vector_store.qdrant_store import build_vectordb, get_collection_name_with_model
from app.config.qdrant_config import qdrant_config

# call qdrant repository which repositories folder
class Indexer:
    """Qdrant-backed indexer for embedding chunks."""

    def __init__(self):
        self.collection_name = get_collection_name_with_model()
        self.vectordb: Optional[QdrantVectorStore] = None

    def initialize_vectordb(self) -> QdrantVectorStore:
        """Initialize Qdrant collection and return vector store.

        Returns:
            Initialized Qdrant vector store.
        """
        self.vectordb = build_vectordb(collection_name=self.collection_name)

        return self.vectordb

    def index_documents(self, chunks: List):
        """Add chunks to Qdrant (initialize if needed).

        Args:
            chunks: List of document chunks.

        Returns:
            Metadata about the indexing operation.
        """
        if not chunks:
            logger.warning("No chunks provided; skipping indexing")
            return

        if self.vectordb is None:
            self.initialize_vectordb()

        try:
            self.vectordb.add_documents(chunks)
            logger.info("Documents added to qdrant vectordb successfully")

            vectordb_info = {"success": True, "collection_name": self.collection_name}

            return vectordb_info

        except Exception as e:
            logger.error("Error adding documents to qdrant vectordb: %s", e)
            raise ValueError(
                f"Error adding documents to qdrant vectordb: {str(e)}"
            ) from e

    def delete_database(self):
        """Delete the vector database.

        Returns:
            Metadata about the deletion.
        """
        client = qdrant_config.get_qdrant_client()
        if self.collection_name not in [col.name for col in client.get_collections().collections]:
            logger.warning("Collection %s not found; skipping deletion", self.collection_name)
            return

        try:
            client.delete_collection(collection_name=self.collection_name)
            logger.info("Vector database deleted successfully")
            return {"success": True, "collection_name": self.collection_name}
        except Exception as e:
            logger.error("Error deleting vector database: %s", e)
            raise ValueError(f"Error deleting vector database: {str(e)}") from e
