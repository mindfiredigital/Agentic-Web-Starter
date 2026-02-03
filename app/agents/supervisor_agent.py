from typing import Optional, Any, Type

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from app.agents.retrieval_agent import RetrievalAgent, RetrievalAgentTool 
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT
from app.services.agent.base_agent import BaseAgent
from app.services.llm.chat_client import ChatClient



class SupervisorAgent(BaseAgent):
    """Supervisor agent that routes requests to tools."""

    def __init__(self) -> None:
        self.retrieve_tool = RetrievalAgentTool(thread_id="")
        
        tools = [self.retrieve_tool]

        super().__init__(llm=ChatClient, tools=tools, system_prompt=SUPERVISOR_PROMPT)

    def handle(self, thread_id: str, query: Optional[str] = None) -> str:
        """Handle a user query with tool execution.

        Args:
            thread_id: Conversation thread identifier.
            query: User query string.

        Returns:
            Agent response output.
        """

        if not query:
            raise ValueError("Provide a query.")

        self.retrieve_tool.thread_id = thread_id

        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": thread_id}},
        )

supervisor = SupervisorAgent()