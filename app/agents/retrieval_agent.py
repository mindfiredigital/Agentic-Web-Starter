from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool

from app.constants.app_constants import VECTOR_DB
from app.prompts.retrieving_prompt import RETRIEVING_PROMPT
from app.services.agent.base_agent import BaseAgent
from app.services.llm.chat_completion_client import ChatModel
from app.tools.retrieving import RetrieveDocumentTool

class RetrievalAgent(BaseAgent):
    def __init__(self) -> None:
        llm = ChatModel().get_chat_model()
        tools = [RetrieveDocumentTool(collection_name=VECTOR_DB.COLLECTION_NAME.value)]
        super().__init__(llm=llm, tools=tools, system_prompt=RETRIEVING_PROMPT)

    def invoke(self, query: str, session_id: str):
        return self.agent_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
