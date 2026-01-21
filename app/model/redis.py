import redis

from src.config.logger import logger
from src.config.settings import settings


def get_redis_client() -> redis.Redis:
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        db=0,
        decode_responses=True,
    )
    logger.info(f"Connected to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    return client