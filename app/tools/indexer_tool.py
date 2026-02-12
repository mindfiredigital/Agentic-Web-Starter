from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.constants.app_constants import VECTOR_DB
from app.utils.core_utils.document import TextProcessor, Indexer

class IndexerTool(BaseTool):
    """Tool that indexes a document into the vector database."""

    name: str = "index_document"
    description: str = "Indexes a document into the vector database"
    filepath: str = Field(exclude=True)

    def _run(self):
        """Execute the indexing tool.

        Loads document, splits into chunks, indexes into Qdrant.

        Returns:
            Dict with success status and collection_name, or None if no chunks.
        """
        text_processor = TextProcessor(file_path=self.filepath)
        
        text = text_processor.load_documents()
        chunks = text_processor.split_documents(text)

        indexer = Indexer()
        index_result = indexer.index_documents(chunks)

        return index_result
