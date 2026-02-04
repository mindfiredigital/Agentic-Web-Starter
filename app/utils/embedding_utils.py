from langchain_huggingface import HuggingFaceEmbeddings

from app.constants.app_constants import VECTOR_DB
from app.config.log_config import logger

class EmbeddingClient:
    """Factory for embeddings clients."""

    def __init__(self, embedding_model_name: str = VECTOR_DB.EMBEDDING_MODEL.value):
        self.embedding_model_name = embedding_model_name

    def create_embeddings(self):
        """Create embeddings client for the vector database.

        Returns:
            HuggingFace embeddings instance.
        """
        # model_name = "sentence-transformers/all-mpnet-base-v2"
        # model_kwargs = {"device": "cpu"}
        encode_kwargs = {"normalize_embeddings": True}
        
        logger.info("Loading embedding model %s (first run may download from Hugging Face)...", self.embedding_model_name)

        model = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            encode_kwargs=encode_kwargs,
        )
        logger.info("Embedding model loaded.")
        return model    

embeddings_client = EmbeddingClient().create_embeddings()