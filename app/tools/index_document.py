from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.constants.app_constants import VECTOR_DB
from app.services.ingestion.text_processor import TextProcessor
from app.services.ingestion.indexer import Indexer

# class IndexDocumentInput(BaseModel):
#     collection_name: str = Field(default=VECTOR_DB.COLLECTION_NAME.value, exclude=True)
#     filepath: str = Field(exclude=True)


class IndexDocumentTool(BaseTool):
    """Tool that indexes a document into the vector database."""

    name: str = "index_document"
    description: str = "Indexes a document into the vector database"
    # args_schema: Type[BaseModel] = IndexDocumentInput
    filepath: str = Field(exclude=True)

    def _run(self):
        """Execute the indexing tool.

        Returns:
            Result of the indexing operation.
        """
        text_processor = TextProcessor(file_path=self.filepath)
        
        text = text_processor.load_documents()
        chunks = text_processor.split_documents(text)

        indexer = Indexer()
        index_result = indexer.index_documents(chunks)

        return index_result
