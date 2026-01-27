from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import BaseTool

from app.services.llm.chat_completion_client import ChatModel
from app.services.memory.redis_history import RedisHistory


class BaseAgent:
    def __init__(self, llm=None, tools: Optional[List[BaseTool]] = None, system_prompt: str = ""):
        self.llm = llm or ChatModel().get_chat_model()
        self.tools = tools or []
        self.system_prompt = system_prompt
        self.redis_history = RedisHistory()
        self.prompt = self.get_prompt()
        self.agent = self.get_agent()
        self.agent_executor = self.get_agent_executor()
        self.agent_with_memory = self.get_agent_with_memory()

    def get_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
    
    def get_agent(self):
        return create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )
    
    def get_agent_executor(self):
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            return_intermediate_steps=True,
        )
    
    def get_agent_with_memory(self):
        return RunnableWithMessageHistory(
            self.agent_executor,
            self.redis_history.get_redis_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="output",
        )