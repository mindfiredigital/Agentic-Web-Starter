from app.config.env_config import settings

def get_default_chat_client():
    """Return the default chat client based on available keys.

    Selection order:
    1) OPENAI_API_KEY presence
    2) GEMINI_API_KEY presence
    """
    if settings.OPENAI_API_KEY:
        from app.llms.openai_chat_client import ChatClient

        return ChatClient().create_client()
        
    if settings.GEMINI_API_KEY:
        from app.llms.gemini_chat_client import ChatClient

        return ChatClient().create_client()

    raise ValueError(
        "No LLM provider configured. Set OPENAI_API_KEY or GEMINI_API_KEY."
    )
