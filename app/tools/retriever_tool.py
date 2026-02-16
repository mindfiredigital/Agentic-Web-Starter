from langchain_core.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from app.config.env_config import settings
from app.services.core_services.retrieval_service import vector_retriever
class RetrieverToolInput(BaseModel):
    query: str = Field(description="The query to retrieve documents from the vector database")
class RetrieverTool(BaseTool):
    """Tool that retrieves documents from the vector database."""

    name: str = "retrieve_documents"
    description: str = "Retrieves documents from the vector database"
    args_schema: Type[BaseModel] = RetrieverToolInput
    collection_name: str = Field(default=settings.COLLECTION_NAME, exclude=True)
    return_direct: bool = False

    def _run(self, query: str):
        """Execute the retrieval tool.

        Args:
            query: Search query string.

        Returns:
            Retrieval result payload.
        """
        vector_retriever.initialize_vectordb()
        contexts = vector_retriever.search(query)
        # contexts = json.dumps([context.page_content for context in contexts])
        return {
            "status": "success",
            "contexts": contexts,
            "collection": self.collection_name
        }
