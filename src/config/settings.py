import os 
from dotenv import load_dotenv
import os
import json 

load_dotenv()

class Settings:
    def __init__(self):
        # Check if SECRETS_JSON is available (used in production)
        secrets_json = os.getenv("SECRETS_JSON")
        self.secrets = {}
        if secrets_json:
            try:
                self.secrets = json.loads(secrets_json)
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON format in SECRETS_JSON") from e
            
        #  LOAD ENVIRONMENT VARIABLES
        self.ENV: str = self.get_env_or_secrets("ENV")
        self.PROJECT_NAME: str = self.get_env_or_secrets("PROJECT_NAME")
        self.PROJECT_VERSION: str = self.get_env_or_secrets("PROJECT_VERSION")
        self.PROJECT_DESCRIPTION: str = self.get_env_or_secrets("PROJECT_DESCRIPTION")
        self.ALLOWED_ORIGINS: list[str] = self.get_env_or_secrets("ALLOWED_ORIGINS", "").split(",")
        self.BASE_PATH: str = self.get_env_or_secrets("BASE_PATH", "")
        self.OPENAI_API_KEY: str = self.get_env_or_secrets("OPENAI_API_KEY")

        self.QDRANT_HOST = self.get_env_or_secrets("QDRANT_HOST", "localhost")
        self.QDRANT_PORT = self.get_env_or_secrets("QDRANT_PORT", "6333")
        
        self.REDIS_HOST = self.get_env_or_secrets("REDIS_HOST", "localhost")
        self.REDIS_PORT = self.get_env_or_secrets("REDIS_PORT", "6379")
        
    def get_env_or_secrets(self, key: str, default: str = None) -> str:
        """
        Get the value of an environment variable or from secrets.
        If not found, return the default value.
        """
        value = os.getenv(key)
        if value is None:
            value = self.secrets.get(key)

        if not value and default is not None:
            return default
        
        if not value:
            raise ValueError(f"Environment variable '{key}' is not set and no default provided.")
        
        return value
    
settings = Settings()