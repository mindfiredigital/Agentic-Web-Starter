from typing import Optional, Any, Type

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from app.agents.retrieval_agent import RetrievalAgent
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT
from app.services.agent.base_agent import BaseAgent
from app.services.llm.chat_client import ChatClient

class RetrievalAgentToolInput(BaseModel):
    query: str = Field(description="The query to retrieve documents from the vector database")

class RetrievalAgentTool(BaseTool):
    name : str = "retriever_agent_tool"
    description: str = "Retrieves an answer for a user question"
    args_schema: Type[BaseModel] = RetrievalAgentToolInput
    retrieval_agent: Any = Field(exclude=True)
    thread_id: str = Field(exclude=True)

    def _run(self, query: str):
        return self.retrieval_agent.invoke(query=query, session_id=self.thread_id)


class SupervisorAgent(BaseAgent):
    def __init__(self) -> None:
        self.retrieval_agent = RetrievalAgent()
        self.retrieve_tool = RetrievalAgentTool(retrieval_agent=self.retrieval_agent, thread_id="")
        tools = [self.retrieve_tool]
        llm = ChatClient().create_client()
        super().__init__(llm=llm, tools=tools, system_prompt=SUPERVISOR_PROMPT)

    def handle(self, thread_id: str, query: Optional[str] = None) -> str:

        if not query:
            raise ValueError("Provide a query.")

        self.retrieve_tool.thread_id = thread_id

        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": thread_id}},
        )
