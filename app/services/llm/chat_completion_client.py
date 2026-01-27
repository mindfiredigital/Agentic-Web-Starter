from langchain_openai import ChatOpenAI
from app.constants.app_constants import CHAT_MODEL

class ChatModel:
    def __init__(self):
        self.model_name = CHAT_MODEL.MODEL_NAME.value
        self.temperature = CHAT_MODEL.TEMPERATURE.value

    def get_chat_model(self):
        return ChatOpenAI(model=self.model_name, temperature=self.temperature)
