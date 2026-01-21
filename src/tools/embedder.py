from langchain_huggingface import HuggingFaceEmbeddings
from src.constants.app_constants import IngestionConstants

embedding_model_name = IngestionConstants.EMBEDDING_MODEL.value
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={"trust_remote_code": True})
