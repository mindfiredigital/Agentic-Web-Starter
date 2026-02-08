"""Document processing utilities.

This module provides document loading, text processing, embedding generation,
file handling, and vector indexing capabilities.
"""

from app.utils.document.embedding_utils import EmbeddingClient, embeddings_client
from app.utils.document.text_processing_utils import TextProcessor
from app.utils.document.file_utils import FileProcessor
from app.utils.document.indexing_utils import Indexer

__all__ = [
    # Classes
    "EmbeddingClient",
    "TextProcessor",
    "FileProcessor",
    "Indexer",
    # Instances
    "embeddings_client",
]
