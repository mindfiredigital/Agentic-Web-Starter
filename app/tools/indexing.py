from typing import List

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


def index_documents(
    documents: List[Document],
    embeddings,
    qdrant_client: QdrantClient,
    collection_name: str,
) -> QdrantVectorStore:
    return QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        client=qdrant_client,
        collection_name=collection_name,
    )
