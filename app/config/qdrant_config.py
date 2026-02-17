from app.config.env_config import settings
from qdrant_client import QdrantClient

class QdrantConfig:
    """Provide Qdrant connection details and helpers."""

    def __init__(self) -> None:
        """Initialize Qdrant config from environment settings."""
        self.host = settings.QDRANT_HOST
        self.port = int(settings.QDRANT_PORT)
        self.collection_name = settings.COLLECTION_NAME
        self.protocol = settings.QDRANT_PROTOCOL
        
    def get_qdrant_client(self):
        """Create and return a Qdrant client.

        Returns:
            QdrantClient instance connected to configured host and port.
        """
        https = self.protocol == "https"
        return QdrantClient(host=self.host, port=self.port, https=https)

    def get_qdrant_url(self) -> str:
        """Return Qdrant URL string.

        Returns:
            Qdrant base URL (e.g., http://host:port).
        """
        return f"{settings.QDRANT_PROTOCOL}://{self.host}:{self.port}"

qdrant_config = QdrantConfig()