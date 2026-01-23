from typing import List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import BaseTool

from app.services.redis_history import get_redis_history
from app.constants.app_constants import VECTOR_DB
from app.prompts.retrieving_prompt import RETRIEVING_PROMPT
from app.tools.retrieving import RetrieveDocumentTool


class RetrievalAgent:
    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        tools: Optional[List[BaseTool]] = None,
    ) -> None:
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.tools = tools or [
            RetrieveDocumentTool(collection_name=VECTOR_DB.COLLECTION_NAME.value)
        ]
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RETRIEVING_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            return_intermediate_steps=True,
        )
        self.agent_with_memory = RunnableWithMessageHistory(
            self.agent_executor,
            get_redis_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="output",
        )

    def invoke(self, query: str, session_id: str):
        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
