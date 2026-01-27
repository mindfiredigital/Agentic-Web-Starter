from langchain_core.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.constants.app_constants import VECTOR_DB
from app.services.retrieval.vector_retriever import VectorRetriever
import json 

class RetrieveDocumentsInput(BaseModel):
    query: str = Field(description="The query to retrieve documents from the vector database")


class RetrieveDocumentsTool(BaseTool):
    name: str = "retrieve_documents"
    description: str = "Retrieves documents from the vector database"
    args_schema: Type[BaseModel] = RetrieveDocumentsInput
    collection_name: str = Field(default=VECTOR_DB.COLLECTION_NAME.value, exclude=True)
    return_direct: bool = False

    def _run(self, query: str):
        retriever = VectorRetriever()
        retriever.initialize_vectordb()
        contexts = retriever.search(query)
        # contexts = json.dumps([context.page_content for context in contexts])
        return {
            "status": "success",
            "contexts": contexts,
            "collection": self.collection_name
        }
