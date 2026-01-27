from app.config.env_config import settings
from redis import Redis

class RedisConfig:
    def __init__(self):
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.db = settings.REDIS_DB
    
    def get_redis_client(self):
        return Redis(
            host=self.host,
            port=self.port,
            db=0,
            decode_responses=True,
        )

    def get_redis_url(self):
        return f"redis://{self.host}:{self.port}/{self.db}"
