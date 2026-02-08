from langchain_community.chat_message_histories import RedisChatMessageHistory
from app.config.redis_config import redis_config
class RedisHistory:
    """Provide Redis-backed chat history instances."""

    def __init__(self):
        self.redis_config = redis_config
        self.redis_url = self.redis_config.get_redis_url()
    
    def get_redis_history(self, session_id: str, ttl: int = 600, key_prefix: str = "agent_chat:") -> RedisChatMessageHistory:
        """Create a chat history store for a session.

        Args:
            session_id: Chat session identifier.
            ttl: Time-to-live in seconds.
            key_prefix: Redis key prefix.

        Returns:
            RedisChatMessageHistory instance.
        """
        return RedisChatMessageHistory(
            session_id=session_id,
            url=self.redis_url,
            ttl=ttl,
            key_prefix=key_prefix,
        )

redis_history = RedisHistory()

