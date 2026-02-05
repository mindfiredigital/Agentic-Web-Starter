import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Load and expose environment settings for the application."""

    def __init__(self):
        #  LOAD ENVIRONMENT VARIABLES

        # 1. Project information
        self.ENV: str = os.getenv("ENV")
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME")
        self.PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
        self.PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION")

        # 2. API configuration
        self.ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "").split(",")
        self.BASE_PATH: str = os.getenv("BASE_PATH", "")
        self.OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        self.GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

        # 3. Authentication configuration
        self.JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

        # 4. Admin configuration
        self.ADMIN_USERNAME: str | None = os.getenv("ADMIN_USERNAME", "").strip() or None
        self.ADMIN_EMAIL: str | None = os.getenv("ADMIN_EMAIL", "").strip() or None
        self.ADMIN_PASSWORD: str | None = os.getenv("ADMIN_PASSWORD", "").strip() or None
        
        # 5. Working directory
        working_dir = os.path.abspath(os.getenv("WORKING_DIR", ".").strip() or ".")

        self.WORKING_PROJECT_DIR: str = os.path.join(working_dir,self.PROJECT_NAME)
        self.DB_PATH: str = os.path.join(working_dir, "sqlite_data", "app.db")
        self.LOG_DIR: str = os.path.join(self.WORKING_PROJECT_DIR, "logs")
        self.UPLOAD_DIR: str = os.path.join(self.WORKING_PROJECT_DIR, "static", "uploads")

        # 6. Hugging Face configuration
        self.HF_HOME: str = os.getenv("HF_HOME", os.path.join(self.WORKING_PROJECT_DIR, "hf"))
        os.environ.setdefault("HF_HOME", self.HF_HOME)

        # 7. Qdrant configuration
        self.COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "agentic_web_starter")

        self.QDRANT_HOST = os.getenv("QDRANT_HOST", "qdrant")
        self.QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
        self.QDRANT_PROTOCOL = os.getenv("QDRANT_PROTOCOL", "http")

        # 8. Redis configuration
        self.REDIS_HOST = os.getenv("REDIS_HOST", "redis")
        self.REDIS_PORT = os.getenv("REDIS_PORT", "6379")
        self.REDIS_PROTOCOL = os.getenv("REDIS_PROTOCOL", "http")
        self.REDIS_DB = os.getenv("REDIS_DB", "0")
        
settings = Settings()