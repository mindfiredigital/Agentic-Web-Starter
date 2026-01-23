from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.constants.app_constants import VECTOR_DB
from app.services.text_processor import TextProcessor
from app.services.vector_indexing import Indexer

class IndexDocumentInput(BaseModel):
    collection_name: str = Field(default=VECTOR_DB.COLLECTION_NAME.value, exclude=True)
    filepath: str = Field(exclude=True)


class IndexDocumentTool(BaseTool):
    name = "index_document"
    description = "Indexes a document into the vector database"
    args_schema: Type[BaseModel] = IndexDocumentInput

    def _run(self, collection_name: str, filepath: str):
        text_processor = TextProcessor(file_path=filepath)
        
        text = text_processor.load_documents()
        chunks = text_processor.split_documents(text)

        indexer = Indexer(collection_name=collection_name)
        indexer.create_database(chunks)

        return {
            "status": "success",
            "chunks_indexed": len(chunks),
            "collection": collection_name
        }
