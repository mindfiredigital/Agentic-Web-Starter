from langchain_huggingface import HuggingFaceEmbeddings
from app.constants.app_constants import VECTOR_DB


def get_embeddings():
    """
    Get the embeddings for the vector database.
    """

    embedding_model_name = VECTOR_DB.EMBEDDING_MODEL.value
    
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={"trust_remote_code": True})
    
    logger.info(f"Embeddings model loaded successfully: {embedding_model_name}")
    
    return embeddings