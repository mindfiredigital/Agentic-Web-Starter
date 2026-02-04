from typing import Optional

from langchain_qdrant import QdrantVectorStore
from qdrant_client import models

from app.config.log_config import logger
from app.config.qdrant_config import QdrantConfig
from app.constants.app_constants import VECTOR_DB
from app.config.env_config import settings
from app.services.llm.embeddings import embeddings_client


def _get_embedding_size() -> int:
    """Return the size of the embedding vectors.

    Returns:
        Embedding vector size.
    """
    embeddings = embeddings_client.embed_query("hello world")
    return len(embeddings)


def _normalize_model_name(model_name: str) -> str:
    """Normalize embedding model name for use in collection names."""
    return model_name.strip().lower().replace("/", "_").replace(" ", "_")


def get_collection_name_with_model() -> str:
    base = settings.COLLECTION_NAME
    model = VECTOR_DB.EMBEDDING_MODEL.value
    return f"{base}_{_normalize_model_name(model)}"


def build_vectordb(
    collection_name: Optional[str] = None,
) -> QdrantVectorStore:
    """Create and return a Qdrant-backed vector store.

    Args:
        collection_name: Optional collection name override.

    Returns:
        Initialized Qdrant vector store.

    Raises:
        ValueError: If Qdrant is unavailable.
    """
    qdrant_config = QdrantConfig()
    client = qdrant_config.get_qdrant_client()
    collection = collection_name or get_collection_name_with_model()
    existing_collections = client.get_collections().collections
    collection_exists = collection in [col.name for col in existing_collections]

    if not collection_exists:
        logger.info("Creating collection %s", collection)
        client.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(
                size=_get_embedding_size(),
                distance=models.Distance.COSINE,
            ),
        )

    try:
        vectordb = QdrantVectorStore(
            client=client,
            collection_name=collection,
            embedding=embeddings_client,
        )
    except Exception as exc:
        logger.error("Error initializing qdrant vectordb: %s", exc)
        raise ValueError(
            "Please make sure qdrant db is running on port 6333: "
            f"{str(exc)}"
        ) from exc

    return vectordb
