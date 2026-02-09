"""Utility modules for the application.

This module provides organized utilities for:
- Auth: Authentication and authorization
- Database: Database connection and management
- Document: Document processing and indexing
- Cache: Caching and session management
"""

# IAM auth utilities
from app.utils.iam_utils.auth import (
    AuthUtils,
    auth_utils,
    JWTUtils,
    JWT_utils,
    JWTError,
    TokenPayload,
    get_current_user_payload,
)

# Database utilities
from app.utils.core_utils.database import (
    SQLiteDatabase,
    sqlite_db,
    get_db,
    init_db,
    utc_now_iso,
)

# Document utilities
from app.utils.core_utils.document import (
    EmbeddingClient,
    embeddings_client,
    TextProcessor,
    FileProcessor,
    Indexer,
)

# Cache utilities
from app.utils.core_utils.cache import (
    RedisHistory,
    redis_history,
)

__all__ = [
    # Auth
    "AuthUtils",
    "auth_utils",
    "JWTUtils",
    "JWT_utils",
    "JWTError",
    "TokenPayload",
    "get_current_user_payload",
    # Database
    "SQLiteDatabase",
    "sqlite_db",
    "get_db",
    "init_db",
    "utc_now_iso",
    # Document
    "EmbeddingClient",
    "embeddings_client",
    "TextProcessor",
    "FileProcessor",
    "Indexer",
    # Cache
    "RedisHistory",
    "redis_history",
]
