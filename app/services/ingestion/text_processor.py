import os 
from typing import List, Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.constants.app_constants import VECTOR_DB, ALLOWED_FILES
from app.config.log_config import logger


class TextProcessor:
    """Load and split documents into chunks."""

    def __init__(
        self,
        file_path: str,
        chunk_size: int = VECTOR_DB.CHUNK_SIZE.value,
        chunk_overlap: int = VECTOR_DB.CHUNK_OVERLAP.value,
        mode: str = VECTOR_DB.LOAD_MODE.value,
        pages_delimiter: str = VECTOR_DB.PAGES_DELIMITER.value,
    ) -> None:
        """
        Initialize the TextProcessor.
        """

        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.mode = mode
        self.pages_delimiter = pages_delimiter
        
    def load_documents(self):
        """Load documents from the file path.

        Returns:
            Loaded document list.

        Raises:
            ValueError: If file extension is invalid.
        """
        
        file_extension = os.path.splitext(self.file_path)[1].lower()
        
        try:
            if file_extension == ALLOWED_FILES.PDF.value:
                loader = PyPDFLoader(self.file_path, mode=self.mode, pages_delimiter=self.pages_delimiter)
            else:
                raise ValueError("Invalid file extension")
            return loader.load() 
        except Exception as e:
            logger.exception("Failed to load documents from %s", self.file_path)
            raise
    

    def split_documents(self, docs) -> List:
        """Split documents into chunks.

        Args:
            docs: Loaded document list.

        Returns:
            List of split documents.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return text_splitter.split_documents(docs)

    def process(self) -> List:
        """Load and split documents.

        Returns:
            List of processed document chunks.
        """
        docs = self.load_documents()
        return self.split_documents(docs)