from app.config.env_config import settings
from redis import Redis

class RedisConfig:
    """Provide Redis connection details and helpers."""

    def __init__(self):
        self.host = settings.REDIS_HOST
        self.port = int(settings.REDIS_PORT)
        self.db = int(settings.REDIS_DB)
    
    def get_redis_client(self):
        """Create and return a Redis client."""
        return Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True,
        )

    def get_redis_url(self):
        """Return Redis URL string."""
        scheme = (settings.REDIS_PROTOCOL or "redis").lower()
        if scheme in {"http", "https"}:
            scheme = "redis"
        return f"{scheme}://{self.host}:{self.port}/{self.db}"
