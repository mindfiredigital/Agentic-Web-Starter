from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.config.env_config import settings


def get_redis_url(db: int = 0) -> str:
    return f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{db}"


def get_redis_history(
    session_id: str,
    ttl: int = 600,
    key_prefix: str = "agent_chat:",
) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id=session_id,
        url=get_redis_url(),
        ttl=ttl,
        key_prefix=key_prefix,
    )
