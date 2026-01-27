from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from app.constants.app_constants import VECTOR_DB
from app.prompts.retrieval_prompt import RETRIEVAL_PROMPT
from app.services.agent.base_agent import BaseAgent
from app.services.llm.chat_client import ChatClient
from app.tools.retrieve_documents import RetrieveDocumentsTool

class RetrievalAgent(BaseAgent):
    def __init__(self) -> None:
        llm = ChatClient().create_client()
        tools = [RetrieveDocumentsTool(collection_name=VECTOR_DB.COLLECTION_NAME.value)]
        super().__init__(llm=llm, tools=tools, system_prompt=RETRIEVAL_PROMPT)

    def invoke(self, query: str, session_id: str):
        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
