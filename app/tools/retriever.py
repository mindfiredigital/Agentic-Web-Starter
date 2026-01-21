from typing import List

from langchain_core.documents import Document
from qdrant_client.models import Filter, FieldCondition, MatchValue


def retrieve_documents(vector_store, query: str, thread_id: str, k: int) -> List[Document]:
    payload_filter = Filter(
        must=[FieldCondition(key="thread_id", match=MatchValue(value=thread_id))]
    )
    return vector_store.similarity_search(
        query=query,
        k=k,
        filter=payload_filter,
    )
