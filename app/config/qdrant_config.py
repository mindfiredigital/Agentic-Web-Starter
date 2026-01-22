from app.constants.app_constants import VectorDB
from app.config.logger import logger
from app.config.env_config import settings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from app.services.embedder import get_embeddings

class QdrantConfig:
    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        self.collection_name = VectorDB.COLLECTION_NAME.value

    def get_qdrant_client(self):
        return QdrantClient(host=self.host, port=self.port)

    def get_vector_store(self):
        embeddings = get_embeddings()
        client = self.get_qdrant_client()

        logger.info(f"Connecting to Qdrant at {self.host}:{self.port}")
        return QdrantVectorStore(
            client=client,
            collection_name=self.collection_name,
            embedding=embeddings,
            retrieval_mode=RetrievalMode.DENSE,
        )