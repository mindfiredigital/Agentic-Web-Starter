from typing import Dict, Any, Optional

from fastapi import UploadFile

from app.config.log_config import logger
from app.utils.file_utils import FileProcessor
from app.tools.indexer_tool import IndexerTool

class IngestionService:
    """Coordinate file storage and indexing."""

    def __init__(self, file: UploadFile) -> None:
        self.file = file

    def save_file(self) -> str:
        """Save the file to the upload directory.

        Returns:
            Saved file path.
        """
        # Initialize file processor with the uploaded file
        file_processor = FileProcessor(file=self.file)

        # Get file path
        file_path = file_processor.get_file_path()

        # Save file
        saved_path = file_processor.save_file(file_path)

        logger.info(f"File saved successfully at: {saved_path}")

        return saved_path

    def ingest_file(self, saved_path: Optional[str] = None) -> Dict[str, Any]:
        """Index the file into the vector database.

        Args:
            saved_path: Optional pre-saved file path.

        Returns:
            Ingestion result with saved path and index metadata.
        """
        if saved_path is None:
            saved_path = self.save_file()

        index_tool = IndexerTool(filepath=saved_path)
        index_result = index_tool._run()

        return {"saved_path": saved_path, "index_result": index_result}
