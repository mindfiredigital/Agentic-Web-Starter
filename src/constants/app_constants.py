from enum import Enum 

class AppConstants(Enum):
    HOST = "127.0.0.1"
    PORT = 3000
    RELOAD = True

class Environment(Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
    
    LOG_DIR = "logs"

class LLM(Enum):
    CHAT_MODEL = "gpt-4o-mini"
    TEMPERATURE = 0.0

class VectorDB(Enum):
    NAME = "agentic_rag_template"
    COLLECTION_NAME = "agentic_rag_template"


class IngestionConstants(Enum):
    CHUNK_SIZE = 100
    CHUNK_OVERLAP = 0

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

class RetrievalConstants(Enum):
    TOP_K = 5

