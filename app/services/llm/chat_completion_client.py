from langchain_openai import ChatOpenAI
from app.config.env_config import settings  
from app.config.redis_config import RedisConfig

class ChatModel:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.temperature = settings.TEMPERATURE

    def get_chat_model(self):
        return ChatOpenAI(model=self.model_name, temperature=self.temperature)
