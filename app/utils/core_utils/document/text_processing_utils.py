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
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_documents(self):
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return text_splitter.split_documents(docs)

    def process(self) -> List:
        docs = self.load_documents()
        return self.split_documents(docs)

