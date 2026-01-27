from langchain_openai import ChatOpenAI

from app.constants.app_constants import CHAT_MODEL


class ChatClient:
    def __init__(self):
        self.model_name = CHAT_MODEL.MODEL_NAME.value
        self.temperature = CHAT_MODEL.TEMPERATURE.value

    def create_client(self):
        return ChatOpenAI(model=self.model_name, temperature=self.temperature)
