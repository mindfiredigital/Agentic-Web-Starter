from typing import Optional, Dict, Any

from fastapi import UploadFile

from app.config.log_config import logger
from app.services.ingestion.file_processor import FileProcessor
from app.services.ingestion.text_processor import TextProcessor
from app.services.ingestion.vector_indexing import Indexer
from app.tools.indexing import IndexDocumentTool

class IngestionService:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def save_file(self) -> str:
        """
        Save the file to the upload directory.
        """
         # Initialize file processor with the uploaded file
        file_processor = FileProcessor(file=self.filepath)

        # Get file path
        file_path = file_processor.get_file_path()

        # Save file
        saved_path = file_processor.save_file(file_path)

        logger.info(f"File saved successfully at: {saved_path}")

        return saved_path

    def ingest(self, saved_path: str) -> Dict[str, Any]:
        """
        Index the file into the vector database.
        """
        # Index file
        index_tool = IndexDocumentTool(filepath=saved_path)
        index_result = index_tool._run()

        return index_result
