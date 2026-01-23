from typing import List, Optional

from langchain_qdrant import QdrantVectorStore
from qdrant_client import models

from app.constants.app_constants import VECTOR_DB
from app.config.qdrant_config import QdrantConfig
from app.services.embedder import Embedder
from app.config.log_config import logger


class Indexer:
    """Qdrant-backed indexer for embedding chunks."""

    def __init__(
        self,
        collection_name: str = VECTOR_DB.COLLECTION_NAME.value,
        embeddings=None,
        qdrant_config: Optional[QdrantConfig] = None,
    ):
        self.embedder_name = VECTOR_DB.EMBEDDING_MODEL.value
        safe_embedder_name = self.embedder_name.replace("/", "_")
        self.collection_name = f"{VECTOR_DB.COLLECTION_NAME.value}__{safe_embedder_name}"
        self.embeddings = Embedder(embedding_model_name=self.embedder_name).get_embeddings()
        self.qdrant_config = qdrant_config or QdrantConfig()
        self.vectordb: Optional[QdrantVectorStore] = None

    def _get_embedding_size(self) -> int:
        """Return the size of the embedding vectors."""
        return len(self.embeddings.embed_query("hello world"))

    def initialize_vectordb(self) -> QdrantVectorStore:
        """Initialize Qdrant collection and return vector store."""
        client = self.qdrant_config.get_qdrant_client()
        existing_collections = client.get_collections().collections

        try:
            if self.collection_name not in [col.name for col in existing_collections]:
                logger.info("Creating collection %s", self.collection_name)
                client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self._get_embedding_size(),
                        distance=models.Distance.COSINE,
                    ),
                )

            self.vectordb = QdrantVectorStore(
                client=client,
                collection_name=self.collection_name,
                embedding=self.embeddings,
            )
        except Exception as e:
            logger.error("Error initializing qdrant vectordb: %s", e)
            raise ValueError(
                "Please make sure qdrant db is running on port 6333: "
                f"{str(e)}"
            ) from e

        return self.vectordb

    def create_database(self, chunks: List):
        """Add chunks to Qdrant (initialize if needed)."""
        if not chunks:
            logger.warning("No chunks provided; skipping indexing")
            return

        if self.vectordb is None:
            self.initialize_vectordb()

        try:
            self.vectordb.add_documents(chunks)
            logger.info("Documents added to qdrant vectordb successfully")

            vectordb_info = {"collection_name": self.collection_name}

            return vectordb_info

        except Exception as e:
            logger.error("Error adding documents to qdrant vectordb: %s", e)
            raise ValueError(
                f"Error adding documents to qdrant vectordb: {str(e)}"
            ) from e

    def delete_database(self):
        """Delete the vector database."""
        client = self.qdrant_config.get_qdrant_client()
        if self.collection_name not in [col.name for col in client.get_collections().collections]:
            logger.warning("Collection %s not found; skipping deletion", self.collection_name)
            return

        try:
            client.delete_collection(collection_name=self.collection_name)
            logger.info("Vector database deleted successfully")
            return {"collection_name": self.collection_name}
        except Exception as e:
            logger.error("Error deleting vector database: %s", e)
            raise ValueError(f"Error deleting vector database: {str(e)}") from e
