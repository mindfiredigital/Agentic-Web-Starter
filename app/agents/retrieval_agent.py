from typing import List, Optional, Type

from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from app.constants.app_constants import VECTOR_DB
from app.prompts.retrieval_prompt import RETRIEVAL_PROMPT
from app.agents.base_agent import BaseAgent
from app.services.llm.chat_client import ChatClient
from app.tools.retrieve_documents import RetrieveDocumentsTool

class RetrievalAgent(BaseAgent):
    """Agent that retrieves documents before answering."""

    def __init__(self) -> None:
        
        tools = [RetrieveDocumentsTool(collection_name=VECTOR_DB.COLLECTION_NAME.value)]
        
        super().__init__(llm=ChatClient, tools=tools, system_prompt=RETRIEVAL_PROMPT)

    def invoke(self, query: str, session_id: str):
        """Run the agent for a query and session.

        Args:
            query: User query.
            session_id: Conversation session identifier.

        Returns:
            Agent response output.
        """
        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )

class RetrievalAgentToolInput(BaseModel):
    query: str = Field(description="The query to retrieve documents from the vector database")

class RetrievalAgentTool(BaseTool):
    """Tool wrapper around the retrieval agent."""
    name : str = "retriever_agent_tool"
    description: str = "Retrieves an answer for a user question"
    args_schema: Type[BaseModel] = RetrievalAgentToolInput
    thread_id: str = Field(exclude=True)

    def _run(self, query: str):
        """Invoke the retrieval agent tool.

        Args:
            query: User query.

        Returns:
            Agent response output.
        """
        retrieval_agent = RetrievalAgent()
        return retrieval_agent.invoke(query=query, session_id=self.thread_id)