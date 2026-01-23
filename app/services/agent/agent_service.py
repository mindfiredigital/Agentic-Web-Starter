from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.services.memory.redis_history import RedisHistory


def BaseAgent:
    def __init__(self, llm, tools, system_prompt):
        self.llm = ChatModel().get_chat_model()
        self.tools = tools
        self.system_prompt = system_prompt
        self.redis_history = RedisHistory()
        
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
            prompt=self.get_prompt(),
        )
    
    def get_agent_executor(self):
        return AgentExecutor(
            agent=self.get_agent(),
            tools=self.tools,
            return_intermediate_steps=True,
        )
    
    def get_agent_with_memory(self):
        return RunnableWithMessageHistory(
            self.get_agent_executor(),
            get_redis_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="output",
        )