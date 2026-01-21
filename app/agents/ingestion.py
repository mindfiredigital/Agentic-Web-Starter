from typing import List

from src.tools.agent_tools import IngestPdfTool


class IngestionAgent:
    def __init__(self) -> None:
        self.tool = IngestPdfTool()

    def ingest(self, thread_id: str, file_paths: List[str]) -> str:
        return self.tool.run({"thread_id": thread_id, "file_paths": file_paths})
