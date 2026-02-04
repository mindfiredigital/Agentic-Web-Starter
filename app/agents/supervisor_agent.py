from typing import Optional

from app.agents.base_agent import BaseAgent
from app.agents.retrieval_agent import RetrievalAgentTool 
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT
from app.services.llm.chat_client import default_chat_client


class SupervisorAgent(BaseAgent):
    """Supervisor agent that routes requests to tools."""

    def __init__(self) -> None:
        self.retrieve_tool = RetrievalAgentTool(thread_id="")
        
        tools = [self.retrieve_tool]

        super().__init__(llm=default_chat_client, tools=tools, system_prompt=SUPERVISOR_PROMPT)

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

        result = self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": thread_id}},
        )
        if isinstance(result, dict) and "output" in result:
            return result["output"]
        return result

supervisor = SupervisorAgent()