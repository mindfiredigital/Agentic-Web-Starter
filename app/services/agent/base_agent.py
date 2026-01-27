from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import BaseTool

from app.services.llm.chat_client import ChatClient
from app.services.memory.redis_history import RedisHistory


class BaseAgent:
    """Base class for tool-calling agents with memory."""

    def __init__(self, llm=None, tools: Optional[List[BaseTool]] = None, system_prompt: str = ""):
        """Initialize the base agent.

        Args:
            llm: LLM client to use.
            tools: Tools available to the agent.
            system_prompt: System prompt string.
        """
        self.llm = llm or ChatClient().create_client()
        self.tools = tools or []
        self.system_prompt = system_prompt
        self.redis_history = RedisHistory()
        self.prompt = self.get_prompt()
        self.agent = self.get_agent()
        self.agent_executor = self.get_agent_executor()
        self.agent_with_memory = self.get_agent_with_memory()

    def get_prompt(self):
        """Build the agent prompt template."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
    
    def get_agent(self):
        """Create the tool-calling agent."""
        return create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )
    
    def get_agent_executor(self):
        """Create the agent executor."""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            return_intermediate_steps=True,
        )
    
    def get_agent_with_memory(self):
        """Create the agent runnable with Redis-backed memory."""
        return RunnableWithMessageHistory(
            self.agent_executor,
            self.redis_history.get_redis_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="output",
        )