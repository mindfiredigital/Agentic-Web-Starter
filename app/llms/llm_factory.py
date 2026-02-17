from app.config.env_config import settings

def get_default_chat_client():
    """Return the default chat client based on available keys.

    Selection order: GEMINI > OPENAI (first non-empty key wins).

    Returns:
        Chat model client (ChatGoogleGenerativeAI or ChatOpenAI).

    Raises:
        ValueError: If neither OPENAI_API_KEY nor GEMINI_API_KEY is set.
    """
    if settings.GEMINI_API_KEY:
        from app.llms.gemini_chat_client import default_chat_client

    elif settings.OPENAI_API_KEY:
        from app.llms.openai_chat_client import default_chat_client
        
    else:
        raise ValueError("No LLM provider configured. Set OPENAI_API_KEY or GEMINI_API_KEY")
        
    return default_chat_client
