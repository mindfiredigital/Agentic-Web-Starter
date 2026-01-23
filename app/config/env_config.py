import os 
from dotenv import load_dotenv
import os
import json 

load_dotenv()

class Settings:
    def __init__(self):
        #  LOAD ENVIRONMENT VARIABLES
        self.ENV: str = os.getenv("ENV")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
        self.PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")
        self.BASE_PATH: str = os.getenv("BASE_PATH", "")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

        self.QDRANT_HOST = "localhost" #os.getenv("QDRANT_HOST", "localhost")
        self.QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
        
        self.REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        self.REDIS_PORT = os.getenv("REDIS_PORT", "6379")
        self.REDIS_DB = os.getenv("REDIS_DB", "0")
        
settings = Settings()