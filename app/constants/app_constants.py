"""Application constants: env names, file types, model config, route paths."""

from enum import Enum


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

    MODEL_NAME = "gemini-2.5-flash-lite"
    TEMPERATURE = 0.0


class VECTOR_DB(Enum):
    """Vector database configuration constants."""

    TOP_K = 5
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

    LOAD_MODE = "page"
    PAGES_DELIMITER = "\n\n"

    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


class ROUTE_CONSTANTS(Enum):
    """API route/path constants shared across the app."""

    API_V1_PREFIX = "/api/v1"
    USER_COMPONENT_URI = "/api/v1/users"
    ROLE_COMPONENT_URI = "/api/v1/roles"
