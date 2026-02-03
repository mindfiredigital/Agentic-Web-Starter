from app.constants.app_constants import VECTOR_DB
from app.config.log_config import logger
from app.config.env_config import settings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, RetrievalMode

class QdrantConfig:
    """Provide Qdrant connection details and helpers."""

    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        self.collection_name = VECTOR_DB.COLLECTION_NAME.value
        self.protocol = settings.QDRANT_PROTOCOL
        
    def get_qdrant_client(self):
        """Create and return a Qdrant client."""
        return QdrantClient(host=self.host, port=self.port)

    def get_qdrant_url(self):
        """Return Qdrant URL string."""
        return f"{settings.QDRANT_PROTOCOL}://{self.host}:{self.port}"
