from app.config.env_config import settings
from app.utils.core_utils.in_memory_utils import in_memory_history
from app.utils.core_utils.redis_utils import redis_history


def get_message_history_factory():
    """Return the configured history factory for agent chat memory."""
    if settings.USE_REDIS:
        return redis_history.get_redis_history
    return in_memory_history.get_history


message_history_factory = get_message_history_factory()
