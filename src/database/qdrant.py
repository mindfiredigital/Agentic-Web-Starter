from qdrant_client import QdrantClient
from src.config.settings import settings
from src.config.logger import logger

def get_qdrant_client():
    logger.info(f"Connecting to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    try:
        return QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
    except Exception as e:
        logger.error(f"Error connecting to Qdrant: {e}")
        raise e
    logger.info(f"Connected to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    return qdrant_client

qdrant_client = get_qdrant_client()