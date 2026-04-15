from typing import Type

from langchain.tools import BaseTool
from pydantic.v1 import BaseModel, Field

from app.agents.base_agent import BaseAgent
from app.config.env_config import settings
from app.llms.llm_factory import get_default_chat_client
from app.prompts.retrieval_prompt import RETRIEVAL_PROMPT
from app.tools.retriever_tool import RetrieverTool


# AGENT
class RetrieverAgent(BaseAgent):
    """Agent that retrieves documents before answering."""

    def __init__(self) -> None:
        """Initialize the retriever agent with retriever tool and retrieval prompt."""
        tools = [RetrieverTool(collection_name=settings.COLLECTION_NAME)]
        super().__init__(
            llm=get_default_chat_client(), tools=tools, system_prompt=RETRIEVAL_PROMPT
        )

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


# TO USE AGENT AS A TOOL
class RetrieverAgentToolInput(BaseModel):
    """Input schema for the retriever agent tool."""

    query: str = Field(
        description="The query to retrieve documents from the vector database"
    )


class RetrieverAgentTool(BaseTool):
    """Tool wrapper around the retrieval agent."""

    name: str = "retriever_agent_tool"
    description: str = "Retrieves an answer for a user question"
    args_schema: Type[BaseModel] = RetrieverAgentToolInput
    thread_id: str = Field(exclude=True)

    def _run(self, query: str):
        """Invoke the retrieval agent tool.

        Args:
            query: User query.

        Returns:
            Agent response output.
        """
        retriever_agent = RetrieverAgent()
        return retriever_agent.invoke(query=query, session_id=self.thread_id)
