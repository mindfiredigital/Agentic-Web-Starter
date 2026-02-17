from typing import Optional

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models

from app.config.log_config import logger
from app.config.qdrant_config import qdrant_config
from app.constants.app_constants import VECTOR_DB
from app.config.env_config import settings
from app.utils.core_utils import embeddings_client


class QdrantRepository:
    """Repository for Qdrant vector database operations."""

    def __init__(self, client: Optional[QdrantClient] = None):
        """Initialize the Qdrant repository.
        
        Args:
            client: Optional QdrantClient instance. If not provided, uses qdrant_config.
        """
        self.client = client or qdrant_config.get_qdrant_client()
        self.embeddings = embeddings_client

    def _get_embedding_size(self) -> int:
        """Return the size of the embedding vectors.

        Returns:
            Embedding vector size.
        """
        embeddings = self.embeddings.embed_query("hello world")
        return len(embeddings)

    def _normalize_model_name(self, model_name: str) -> str:
        """Normalize embedding model name for use in collection names.
        
        Args:
            model_name: Model name to normalize.
            
        Returns:
            Normalized model name.
        """
        return model_name.strip().lower().replace("/", "_").replace(" ", "_")

    def get_collection_name_with_model(self) -> str:
        """Get collection name with embedded model name.
        
        Returns:
            Collection name including model identifier.
        """
        base = settings.COLLECTION_NAME
        model = VECTOR_DB.EMBEDDING_MODEL.value
        return f"{base}_{self._normalize_model_name(model)}"

    def build_vectordb(self, collection_name: Optional[str] = None) -> QdrantVectorStore:
        """Create and return a Qdrant-backed vector store.

        Args:
            collection_name: Optional collection name override.

        Returns:
            Initialized Qdrant vector store.

        Raises:
            ValueError: If Qdrant is unavailable.
        """
        collection = collection_name or self.get_collection_name_with_model()
        existing_collections = self.client.get_collections().collections
        collection_exists = collection in [col.name for col in existing_collections]

        if not collection_exists:
            logger.info("Creating collection %s", collection)
            self.client.create_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(
                    size=self._get_embedding_size(),
                    distance=models.Distance.COSINE,
                ),
            )

        try:
            vectordb = QdrantVectorStore(
                client=self.client,
                collection_name=collection,
                embedding=self.embeddings,
            )
        except Exception as exc:
            logger.error("Error initializing qdrant vectordb: %s", exc)
            raise ValueError(
                "Please make sure qdrant db is running on port 6333: "
                f"{str(exc)}"
            ) from exc

        return vectordb

    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection from Qdrant.
        
        Args:
            collection_name: Name of the collection to delete.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.client.delete_collection(collection_name=collection_name)
            logger.info("Collection %s deleted successfully", collection_name)
            return True
        except Exception as exc:
            logger.error("Error deleting collection %s: %s", collection_name, exc)
            raise ValueError(f"Error deleting collection: {str(exc)}") from exc

    def collection_exists(self, collection_name: str) -> bool:
        """Check if a collection exists in Qdrant.
        
        Args:
            collection_name: Name of the collection to check.
            
        Returns:
            True if collection exists, False otherwise.
        """
        existing_collections = self.client.get_collections().collections
        return collection_name in [col.name for col in existing_collections]


# Create a singleton instance for backward compatibility
qdrant_repository = QdrantRepository()
