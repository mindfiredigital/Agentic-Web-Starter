from langchain_openai import ChatOpenAI

from app.constants.app_constants import CHAT_MODEL


class ChatClient:
    """Factory for chat model clients."""

    def __init__(self):
        self.model_name = CHAT_MODEL.MODEL_NAME.value
        self.temperature = CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        """Create a chat model client.

        Returns:
            ChatOpenAI instance.
        """
        return ChatOpenAI(model=self.model_name, temperature=self.temperature)

default_chat_client = ChatClient().create_client()