from typing import Optional, List

from langchain_qdrant import QdrantVectorStore

from app.constants.app_constants import VECTOR_DB
from app.config.qdrant_config import QdrantConfig
from app.services.embedder import Embedder
from app.config.log_config import logger


class Retriever:
    """Qdrant-backed retriever for existing collections."""

    def __init__(self, collection_name: Optional[str] = None):
        # self.embedder_name = VECTOR_DB.EMBEDDING_MODEL.value
        # safe_embedder_name = self.embedder_name.replace("/", "_")
        self.collection_name = collection_name or VECTOR_DB.COLLECTION_NAME.value
        self.embeddings = Embedder().get_embeddings()
        self.qdrant_config = QdrantConfig()
        self.vectordb: Optional[QdrantVectorStore] = None
        self.top_k = VECTOR_DB.TOP_K.value

    def initialize_vectordb(self) -> QdrantVectorStore:
        """Connect to an existing Qdrant collection."""
        client = self.qdrant_config.get_qdrant_client()
        existing_collections = client.get_collections().collections

        if self.collection_name not in [col.name for col in existing_collections]:
            raise ValueError(
                f"Collection '{self.collection_name}' not found. "
                "Run indexing first to create it."
            )

        try:
            self.vectordb = QdrantVectorStore(
                client=client,
                collection_name=self.collection_name,
                embedding=self.embeddings,
            )
        except Exception as e:
            logger.error("Error initializing qdrant retriever: %s", e)
            raise ValueError(
                "Please make sure qdrant db is running on port 6333: "
                f"{str(e)}"
            ) from e

        return self.vectordb

    def similarity_search(self, query: str):
        """Return top-k documents matching the query."""
        if not query:
            logger.warning("Empty query provided; returning no results")
            return []

        if self.vectordb is None:
            self.initialize_vectordb()

        try:
            return self.vectordb.similarity_search(query, k=self.top_k)
        except Exception as e:
            logger.error("Error querying qdrant vectordb: %s", e)
            raise ValueError(f"Error querying qdrant vectordb: {str(e)}") from e

    