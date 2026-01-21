from typing import List, Optional

from src.agents.ingestion import IngestionAgent
from src.agents.response import ResponseAgent


class SupervisorAgent:
    def __init__(self) -> None:
        self.ingestion_agent = IngestionAgent()
        self.response_agent = ResponseAgent()

    def handle(
        self,
        thread_id: str,
        query: Optional[str] = None,
        file_paths: Optional[List[str]] = None,
    ) -> str:
        if file_paths:
            return self.ingestion_agent.ingest(thread_id=thread_id, file_paths=file_paths)
        if not query:
            raise ValueError("Query is required when no files are provided.")
        return self.response_agent.answer(thread_id=thread_id, query=query)
