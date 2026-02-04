from app.config.env_config import settings
from qdrant_client import QdrantClient

class QdrantConfig:
    """Provide Qdrant connection details and helpers."""

    def __init__(self):
        self.host = settings.QDRANT_HOST
        self.port = int(settings.QDRANT_PORT)
        self.collection_name = settings.COLLECTION_NAME
        self.protocol = settings.QDRANT_PROTOCOL
        
    def get_qdrant_client(self):
        """Create and return a Qdrant client."""
        https = self.protocol == "https"
        return QdrantClient(host=self.host, port=self.port, https=https)

    def get_qdrant_url(self):
        """Return Qdrant URL string."""
        return f"{settings.QDRANT_PROTOCOL}://{self.host}:{self.port}"

qdrant_config = QdrantConfig()