import os 
from typing import List, Optional

from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.constants.app_constants import VECTOR_DB
from app.config.logger import logger


class TextProcessor:
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
        """
        Load the documents from the file path.
        """
        try:
            if self.file_extension == ALLOWED_FILES.PDF.value:
                loader = PyPDFLoader(self.file_path, mode=self.mode, pages_delimiter=self.pages_delimiter)
            else:
                raise HTTPException(status_code=400, detail="Invalid file extension")
            return loader.load() 

    def split_documents(self, docs) -> List:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        return text_splitter.split_documents(docs)

    def process(self) -> List:
        """
        Process the documents.
        """
        docs = self.load_documents()
        return self.split_documents(docs)