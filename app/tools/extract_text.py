from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader, PyPDFLoader
from src.config.logger import logger


def load_pdf_documents(file_path: str) -> List[Document]:
    """
    Load a PDF into LangChain Documents.
    Uses PyMuPDFLoader first, falls back to PyPDFLoader.
    """
    try:
        logger.info(f"Loading PDF with PyMuPDFLoader: {file_path}")
        return PyMuPDFLoader(file_path).load()
    except Exception as exc:
        logger.warning(f"PyMuPDFLoader failed, falling back to PyPDFLoader: {exc}")
        return PyPDFLoader(file_path).load()