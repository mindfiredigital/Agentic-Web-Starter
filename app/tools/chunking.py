from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.constants.app_constants import IngestionConstants


def chunk_documents(
    documents: List[Document],
    chunk_size: int = IngestionConstants.CHUNK_SIZE.value,
    chunk_overlap: int = IngestionConstants.CHUNK_OVERLAP.value,
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)