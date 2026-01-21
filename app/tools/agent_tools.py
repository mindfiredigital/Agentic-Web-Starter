from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from src.config.database import QDRANT_COLLECTION
from src.constants.app_constants import RetrievalConstants
from src.database.qdrant import get_qdrant_client, get_vector_store
from src.services.embedder import get_embeddings
from src.tools.chunking import chunk_documents
from src.tools.extract_text import load_pdf_documents
from src.tools.indexing import index_documents
from src.tools.response_generator import generate_answer
from src.tools.retriever import retrieve_documents


class IngestPdfArgs(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    file_paths: List[str] = Field(..., description="Local PDF file paths")


class IngestPdfTool(BaseTool):
    name: str = "ingest_pdf_tool"
    description: str = "Load PDFs, chunk, embed, and index them in Qdrant."
    args_schema = IngestPdfArgs

    def _run(self, thread_id: str, file_paths: List[str]) -> str:
        qdrant_client = get_qdrant_client()
        embeddings = get_embeddings()
        all_docs: List[Document] = []
        for file_path in file_paths:
            docs = load_pdf_documents(file_path)
            for doc in docs:
                doc.metadata = {
                    **(doc.metadata or {}),
                    "thread_id": thread_id,
                    "source": file_path,
                }
            all_docs.extend(docs)

        chunks = chunk_documents(all_docs)
        index_documents(
            documents=chunks,
            embeddings=embeddings,
            qdrant_client=qdrant_client,
            collection_name=QDRANT_COLLECTION,
        )
        return f"Indexed {len(chunks)} chunks into {QDRANT_COLLECTION}."


class RetrieveArgs(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    query: str = Field(..., description="User query")
    k: int = Field(default=RetrievalConstants.TOP_K.value, ge=1, le=20)


class RetrieveTool(BaseTool):
    name: str = "retrieve_tool"
    description: str = "Retrieve relevant chunks from Qdrant for a thread."
    args_schema = RetrieveArgs

    def _run(self, thread_id: str, query: str, k: int) -> List[Document]:
        vector_store = get_vector_store()
        return retrieve_documents(vector_store, query=query, thread_id=thread_id, k=k)


class GenerateAnswerArgs(BaseModel):
    thread_id: str = Field(..., description="Conversation thread id")
    query: str = Field(..., description="User query")
    contexts: List[Document] = Field(..., description="Retrieved documents")
    history: str = Field(default="", description="Conversation history text")


class GenerateAnswerTool(BaseTool):
    name: str = "generate_answer_tool"
    description: str = "Generate an answer from context and conversation history."
    args_schema = GenerateAnswerArgs

    def _run(
        self,
        thread_id: str,
        query: str,
        contexts: List[Document],
        history: str = "",
    ) -> str:
        _ = thread_id  # thread_id used for tracing, not needed in generation call
        return generate_answer(query=query, documents=contexts, history_text=history)

