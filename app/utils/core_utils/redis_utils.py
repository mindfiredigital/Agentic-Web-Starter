from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.config.redis_config import redis_config


class RedisHistory:
    """Provide Redis-backed chat history instances."""

    def __init__(self) -> None:
        """Initialize Redis history from config."""
        self.redis_config = redis_config
        self.redis_url = self.redis_config.get_redis_url()

    def get_redis_history(
        self, session_id: str, key_prefix: str = "agent_chat:"
    ) -> RedisChatMessageHistory:
        """Create a chat history store for a session.

        Args:
            session_id: Unique identifier for the conversation session.
            ttl: Time-to-live for history entries in seconds. Defaults to 600.
            key_prefix: Redis key prefix. Defaults to "agent_chat:".

        Returns:
            RedisChatMessageHistory instance for the session.
        """
        return RedisChatMessageHistory(
            session_id=session_id,
            url=self.redis_url,
            key_prefix=key_prefix,
        )


redis_history = RedisHistory()
