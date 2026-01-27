from langchain_huggingface import HuggingFaceEmbeddings

from app.constants.app_constants import VECTOR_DB

_EMBEDDINGS_CLIENT = None


class EmbeddingClient:
    """Factory for embeddings clients."""

    def __init__(self, embedding_model_name: str = VECTOR_DB.EMBEDDING_MODEL.value):
        self.embedding_model_name = embedding_model_name

    def create_embeddings(self):
        """Create embeddings client for the vector database.

        Returns:
            HuggingFace embeddings instance.
        """
        return HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={"trust_remote_code": True},
        )


def get_embeddings_client():
    """Return a cached embeddings client instance.

    Returns:
        HuggingFace embeddings instance.
    """
    global _EMBEDDINGS_CLIENT
    if _EMBEDDINGS_CLIENT is None:
        _EMBEDDINGS_CLIENT = EmbeddingClient().create_embeddings()
    return _EMBEDDINGS_CLIENT
