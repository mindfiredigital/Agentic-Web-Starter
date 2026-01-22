from langchain_huggingface import HuggingFaceEmbeddings
from app.constants.app_constants import VECTOR_DB


class Embedder:
    def __init__(self, embedding_model_name: str = VECTOR_DB.EMBEDDING_MODEL.value):
        self.embedding_model_name = embedding_model_name

    def get_embeddings(self):
        """
        Get the embeddings for the vector database.
        """
        return HuggingFaceEmbeddings(model_name=self.embedding_model_name, model_kwargs={"trust_remote_code": True})
    