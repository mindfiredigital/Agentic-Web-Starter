import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.log_config import logger
from app.constants.app_constants import ALLOWED_FILES, VECTOR_DB


class TextProcessor:
    """Load and split documents into chunks."""

    def __init__(
        self,
        file_path: str,
        chunk_size: int = VECTOR_DB.CHUNK_SIZE.value,
        chunk_overlap: int = VECTOR_DB.CHUNK_OVERLAP.value,
    ) -> None:
        """Initialize text processor for a file.

        Args:
            file_path: Path to the document file.
            chunk_size: Size of each text chunk. Defaults to VECTOR_DB setting.
            chunk_overlap: Overlap between chunks. Defaults to VECTOR_DB setting.
        """
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_documents(self):
        """Load documents from the file based on extension.

        Returns:
            List of loaded Document objects.

        Raises:
            ValueError: If file extension is unsupported.
        """
        file_extension = os.path.splitext(self.file_path)[1].lower()

        try:
            if file_extension == ALLOWED_FILES.PDF.value:
                loader = PyPDFLoader(self.file_path)
            else:
                raise ValueError("Invalid file extension")
            return loader.load()
        except Exception:
            logger.exception("Failed to load documents from %s", self.file_path)
            raise

    def split_documents(self, docs) -> List:
        """Split documents into chunks.

        Args:
            docs: List of documents loaded from the file to split.

        Returns:
            List of document chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(docs)

    def process(self) -> List:
        """Load and split documents in one step.

        Returns:
            List of document chunks ready for indexing.
        """
        docs = self.load_documents()
        return self.split_documents(docs)
