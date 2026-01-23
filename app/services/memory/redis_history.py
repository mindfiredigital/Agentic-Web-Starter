from langchain_community.chat_message_histories import RedisChatMessageHistory
from app.config.redis_config import RedisConfig
from app.config.env_config import settings


class RedisHistory:
    def __init__(self):
        self.redis_config = RedisConfig()
        self.redis_url = self.redis_config.get_redis_url()
    
    def get_redis_history(self, session_id: str, ttl: int = 600, key_prefix: str = "agent_chat:") -> RedisChatMessageHistory:
        return RedisChatMessageHistory(
            session_id=session_id,
            url=self.redis_url,
            ttl=ttl,
            key_prefix=key_prefix,
        )

