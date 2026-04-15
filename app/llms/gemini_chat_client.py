from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.env_config import settings
from app.constants.app_constants import GEMINI_CHAT_MODEL


class GeminiChatClient:
    """Factory for Gemini chat model clients."""

    def __init__(self) -> None:
        """Initialize with model name and temperature from constants."""
        self.model_name = GEMINI_CHAT_MODEL.MODEL_NAME.value
        self.temperature = GEMINI_CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        """Create a Gemini chat model client.

        Returns:
            ChatGoogleGenerativeAI instance.
        """
        chat_client = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            include_thoughts=True,
            google_api_key=settings.GEMINI_API_KEY,
        )
        return chat_client


default_chat_client = GeminiChatClient().create_client()
