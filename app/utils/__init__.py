"""Utility modules for the application.

This module provides organized utilities for:
- Auth: Authentication and authorization
- Database: Database connection and management
- Document: Document processing and indexing
- Cache: Caching and session management
"""

# IAM auth utilities
from app.utils.iam_utils import (
    AuthUtils,
    auth_utils,
    JWTUtils,
    JWT_utils,
    JWTError,
    TokenPayload,
    get_current_user_payload,
)

# Core utilities (database, document, cache)
from app.utils.core_utils import (
    SQLiteDatabase,
    sqlite_db,
    get_db,
    init_db,
    utc_now_iso,
    EmbeddingClient,
    embeddings_client,
    TextProcessor,
    FileProcessor,
    Indexer,
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
