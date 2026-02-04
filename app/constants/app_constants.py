from enum import Enum 

class AppConstants(Enum):
    """Generic application constants."""

    HOST = "127.0.0.1"
    PORT = 3000
    RELOAD = True

class Environment(Enum):
    """Environment names and path constants."""

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    
class ALLOWED_FILES(Enum):
    """Supported file extensions for ingestion."""

    PDF = ".pdf"
    DOCX = ".docx"
    ALL_FILES = (".pdf", ".docx")

class OPENAI_CHAT_MODEL(Enum):
    """Chat model configuration."""

    MODEL_NAME = "gpt-4o-mini"
    TEMPERATURE = 0.0

class GEMINI_CHAT_MODEL(Enum):
    """Gemini chat model configuration."""

    MODEL_NAME = "gemini-2.5-flash"
    TEMPERATURE = 0.0

class VECTOR_DB(Enum):
    """Vector database configuration constants."""

    NAME = "agentic_rag_template"
    COLLECTION_NAME = "agentic_rag_template"

    TOP_K = 5
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50 
    
    LOAD_MODE = "page"
    PAGES_DELIMITER = "\n\n"
    
    # EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    # EMBEDDING_MODEL = "mixedbread-ai/mxbai-embed-large-v1"
    # EMBEDDING_MODEL = "BAAI/bge-m3"
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

    
    # PERSIST_DIR = "static/vector_db_stores/qdrant_store"




