"""Repository layer for data access.

This module provides organized access to:
- SQL: Relational database repositories
- Vector: Vector database repositories for embeddings
"""

# SQL repositories
from app.repository.sql_repository import (
    ACLRepository,
    BaseRepository,
    ComponentRepository,
    RoleRepository,
    UserRepository,
)

# Vector repositories
from app.repository.vector_repository import qdrant_repository

__all__ = [
    # SQL
    "BaseRepository",
    "UserRepository",
    "RoleRepository",
    "ComponentRepository",
    "ACLRepository",
    # Vector
    "qdrant_repository",
]
