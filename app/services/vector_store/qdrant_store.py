from typing import Optional

from langchain_qdrant import QdrantVectorStore
from qdrant_client import models

from app.config.log_config import logger
from app.config.qdrant_config import QdrantConfig
from app.constants.app_constants import VECTOR_DB
from app.services.llm.embeddings import get_embeddings_client


def _get_embedding_size() -> int:
    """Return the size of the embedding vectors."""
    embeddings = get_embeddings_client()
    return len(embeddings.embed_query("hello world"))


def build_vectordb(
    collection_name: Optional[str] = None,
    ensure_collection: bool = False,
) -> QdrantVectorStore:
    """
    Create and return a Qdrant-backed vector store.

    If ensure_collection is True, create the collection when missing.
    Otherwise, raise if the collection does not exist.
    """
    qdrant_config = QdrantConfig()
    client = qdrant_config.get_qdrant_client()
    collection = collection_name or VECTOR_DB.COLLECTION_NAME.value
    existing_collections = client.get_collections().collections
    collection_exists = collection in [col.name for col in existing_collections]

    if ensure_collection and not collection_exists:
        logger.info("Creating collection %s", collection)
        client.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(
                size=_get_embedding_size(),
                distance=models.Distance.COSINE,
            ),
        )
    elif not ensure_collection and not collection_exists:
        raise ValueError(
            f"Collection '{collection}' not found. Run indexing first to create it."
        )

    try:
        vectordb = QdrantVectorStore(
            client=client,
            collection_name=collection,
            embedding=get_embeddings_client(),
        )
    except Exception as exc:
        logger.error("Error initializing qdrant vectordb: %s", exc)
        raise ValueError(
            "Please make sure qdrant db is running on port 6333: "
            f"{str(exc)}"
        ) from exc

    return vectordb
