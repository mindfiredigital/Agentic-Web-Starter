from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from src.config.database import QDRANT_COLLECTION
from src.config.logger import logger
from src.config.settings import settings
from src.services.embedder import get_embeddings


def get_qdrant_client() -> QdrantClient:
    logger.info(f"Connecting to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)


def get_vector_store(collection_name: str = QDRANT_COLLECTION) -> QdrantVectorStore:
    client = get_qdrant_client()
    embeddings = get_embeddings()
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
    )