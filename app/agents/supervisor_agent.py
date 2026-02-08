from typing import Optional

from app.agents.base_agent import BaseAgent
from app.agents.retriever_agent import RetrieverAgentTool
from app.config.log_config import logger
from app.exceptions import InternalError, ValidationError
from app.llms.llm_factory import get_default_chat_client
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT


class SupervisorAgent(BaseAgent):
    """Supervisor agent that routes requests to tools."""

    def __init__(self) -> None:
        self.retrieve_tool = RetrieverAgentTool(thread_id="")
        tools = [self.retrieve_tool]
        super().__init__(llm=get_default_chat_client(), tools=tools, system_prompt=SUPERVISOR_PROMPT)

    def invoke(self, thread_id: str, query: Optional[str] = None) -> str:
        """Handle a user query with tool execution.

        Args:
            thread_id: Conversation thread identifier.
            query: User query string.

        Returns:
            Agent response output.
        """
        if not query:
            raise ValidationError("Provide a query.")

        self.retrieve_tool.thread_id = thread_id
        try:
            result = self.agent_with_memory.invoke(
                {"input": query},
                config={"configurable": {"session_id": thread_id}},
            )
            if isinstance(result, dict) and "output" in result:
                return result["output"]
            return result
        except (ValidationError, InternalError):
            raise
        except Exception as e:
            logger.exception("Chat/agent invocation failed: %s", e)
            raise InternalError("Chat request failed") from e


supervisor = SupervisorAgent()