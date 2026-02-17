from langchain_openai import ChatOpenAI
from app.config.env_config import settings
from app.constants.app_constants import OPENAI_CHAT_MODEL


class OpenAIChatClient:
    """Factory for OpenAI chat model clients."""

    def __init__(self) -> None:
        """Initialize with model name and temperature from constants."""
        self.model_name = OPENAI_CHAT_MODEL.MODEL_NAME.value
        self.temperature = OPENAI_CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        """Create a chat model client.

        Returns:
            ChatOpenAI instance.
        """
        chat_client = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY
        )
        return chat_client

default_chat_client = OpenAIChatClient().create_client()