from typing import List, Optional, Any, Type

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from app.agents.ingestion import IngestionAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.prompts.supervisor_prompt import SUPERVISOR_PROMPT
from app.services.agent.agent_service import BaseAgent

class RetrieveAnswerInput(BaseModel):
    query: str = Field(exclude=True)


class IngestDocumentsTool(BaseTool):
    name = "ingest_documents"
    description = "Indexes provided documents into the vector database"
    ingestion_agent: Any = Field(exclude=True)
    thread_id: str = Field(exclude=True)
    
    def _run(self, thread_id: str):
        return self.ingestion_agent.ingest(thread_id=self.thread_id)


class RetrieveAnswerTool(BaseTool):
    name = "retrieve_answer"
    description = "Retrieves an answer for a user question"
    args_schema: Type[BaseModel] = RetrieveAnswerInput
    thread_id: str = Field(exclude=True)

    def _run(self, query: str):
        return self.retrieval_agent.invoke(query=query, session_id=self.thread_id)


class SupervisorAgent(BaseAgent):
    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
    ) -> None:
        self.ingestion_agent = IngestionAgent()
        self.retrieval_agent = RetrievalAgent()
        tools = [
            IngestDocumentsTool(thread_id=thread_id),
            RetrieveAnswerTool(thread_id=thread_id),
        ]
        llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
        super().__init__(llm=llm, tools=tools, system_prompt=SUPERVISOR_PROMPT)

    def handle(
        self,
        thread_id: str,
        query: Optional[str] = None,
        file_paths: Optional[List[str]] = None,
    ) -> str:
        if not query and not file_paths:
            raise ValueError("Provide a query or file paths.")

        input_parts = [f"thread_id: {thread_id}"]
        if query:
            input_parts.append(f"query: {query}")
        if file_paths:
            input_parts.append(f"file_paths: {file_paths}")

        return self.agent_with_memory.invoke(
            {"input": "\n".join(input_parts)},
            config={"configurable": {"session_id": thread_id}},
        )
