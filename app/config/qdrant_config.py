from app.constants.app_constants import VECTOR_DB
from app.config.log_config import logger
from app.config.env_config import settings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, RetrievalMode

class QdrantConfig:
    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        self.collection_name = VECTOR_DB.COLLECTION_NAME.value

    def get_qdrant_client(self):
        return QdrantClient(host=self.host, port=self.port)

    def get_qdrant_url(self):
        return f"http://{self.host}:{self.port}"
