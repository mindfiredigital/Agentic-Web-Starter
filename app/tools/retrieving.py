from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.constants.app_constants import VECTOR_DB
from app.services.retriever import Retriever
import json 

class RetrieveDocumentInput(BaseModel):
    query: str = Field(description="The query to retrieve documents from the vector database")


class RetrieveDocumentTool(BaseTool):
    name: str = "retrieve_document"
    description: str = "Retrieves a document from the vector database"
    args_schema: Type[BaseModel] = RetrieveDocumentInput
    collection_name: str = Field(default=VECTOR_DB.COLLECTION_NAME.value, exclude=True)
    return_direct: bool = False

    def _run(self, query: str):
        retriever = Retriever(self.collection_name)
        retriever.initialize_vectordb()
        contexts = retriever.similarity_search(query)
        contexts = json.dumps([context.page_content for context in contexts])
        return {
            "status": "success",
            "contexts": contexts,
            "collection": self.collection_name
        }
