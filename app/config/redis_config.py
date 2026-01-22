from src.config.settings import settings
import redis 

class RedisConfig:
    def __init__(self):
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT

    def get_redis_client(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=0,
            decode_responses=True,
        )
