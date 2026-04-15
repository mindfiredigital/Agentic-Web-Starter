"""Utility modules for the application.

This module provides organized utilities for:
- Auth: Authentication and authorization
- Database: Database connection and management
- Document: Document processing and indexing
- Cache: Caching and session management
"""

# Core utilities (database, document, cache)
from app.utils.core_utils import (
    EmbeddingClient,
    FileProcessor,
    Indexer,
    InMemoryHistory,
    RedisHistory,
    SQLiteDatabase,
    TextProcessor,
    embeddings_client,
    get_db,
    in_memory_history,
    init_db,
    message_history_factory,
    redis_history,
    sqlite_db,
    utc_now_iso,
)

# IAM auth utilities
from app.utils.iam_utils import (
    AuthUtils,
    JWT_utils,
    JWTError,
    JWTUtils,
    TokenPayload,
    auth_utils,
    get_current_user_payload,
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
    "InMemoryHistory",
    "in_memory_history",
    "message_history_factory",
]
