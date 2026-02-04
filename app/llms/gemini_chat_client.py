import importlib

from app.constants.app_constants import GEMINI_CHAT_MODEL


class ChatClient:
    """Factory for Gemini chat model clients."""

    def __init__(self):
        self.model_name = GEMINI_CHAT_MODEL.MODEL_NAME.value
        self.temperature = GEMINI_CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        """Create a Gemini chat model client.

        Returns:
            ChatGoogleGenerativeAI instance.
        """
        try:
            module = importlib.import_module("langchain_google_genai")
        except ImportError as exc:
            raise ImportError(
                "langchain-google-genai is required for Gemini chat client. "
                "Install with `pip install langchain-google-genai`."
            ) from exc

        chat_client = getattr(module, "ChatGoogleGenerativeAI", None)
        if chat_client is None:
            raise ImportError(
                "ChatGoogleGenerativeAI not found in langchain_google_genai."
            )

        return chat_client(model=self.model_name, temperature=self.temperature)


default_chat_client = ChatClient().create_client()
