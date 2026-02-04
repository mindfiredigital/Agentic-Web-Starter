import os
import json
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Load and expose environment settings for the application."""

    def __init__(self):
        #  LOAD ENVIRONMENT VARIABLES
        working_dir = os.getenv("WORKING_DIR", ".").strip() or "."
        working_dir = os.path.abspath(working_dir)

        self.ENV: str = os.getenv("ENV")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
        self.PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")
        self.BASE_PATH: str = os.getenv("BASE_PATH", "")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.WORKING_DIR: str = working_dir
        self.LOG_DIR: str = os.path.join(working_dir, "logs")
        self.UPLOAD_DIR: str = os.path.join(working_dir, "app", "static", "uploads")
        self.PERSIST_DIR: str = os.path.join(
            working_dir,
            "static",
            "vector_db_stores",
            "qdrant_store",
        )
        self.COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "agentic_rag_template")

        self.QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
        self.QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
        self.QDRANT_PROTOCOL = os.getenv("QDRANT_PROTOCOL", "http")
        
        self.REDIS_HOST = os.getenv("REDIS_HOST", "redis")
        self.REDIS_PORT = os.getenv("REDIS_PORT", "6379")
        self.REDIS_PROTOCOL = os.getenv("REDIS_PROTOCOL", "http")
        self.REDIS_DB = os.getenv("REDIS_DB", "0")
        
settings = Settings()