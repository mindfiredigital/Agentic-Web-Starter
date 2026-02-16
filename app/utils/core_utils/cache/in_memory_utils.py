from langchain_core.chat_history import InMemoryChatMessageHistory


class InMemoryHistory:
    """Provide in-memory chat history instances keyed by session id."""

    def __init__(self) -> None:
        self._store: dict[str, InMemoryChatMessageHistory] = {}

    def get_history( self, session_id: str,) -> InMemoryChatMessageHistory:
        """Create or fetch a chat history store for a session.

        Args:
            session_id: Conversation session identifier.
            ttl: Unused; accepted for API parity with Redis history provider.
            key_prefix: Unused; accepted for API parity with Redis provider.
        """
        if session_id not in self._store:
            self._store[session_id] = InMemoryChatMessageHistory()
        return self._store[session_id]

in_memory_history = InMemoryHistory()
