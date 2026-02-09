from typing import Any, Dict, Optional

from fastapi import UploadFile

from app.config.log_config import logger
from app.exceptions import InternalError, ValidationError
from app.tools.indexer_tool import IndexerTool
from app.utils.core_utils.document import FileProcessor


class IngestionService:
    """Coordinate file storage and indexing."""

    def __init__(self, file: UploadFile) -> None:
        self.file = file

    def save_file(self) -> str:
        """Save the file to the upload directory.

        Returns:
            Saved file path.
        """
        try:
            file_processor = FileProcessor(file=self.file)
            file_path = file_processor.get_file_path()
            saved_path = file_processor.save_file(file_path)
            logger.info("File saved successfully at: %s", saved_path)
            return saved_path
        except (OSError, IOError) as e:
            logger.exception("File save failed: %s", e)
            raise ValidationError("File save failed") from e
        except Exception as e:
            logger.exception("Unexpected error saving file: %s", e)
            raise InternalError("File upload failed") from e

    def ingest_file(self, saved_path: Optional[str] = None) -> Dict[str, Any]:
        """Index the file into the vector database.

        Args:
            saved_path: Optional pre-saved file path.

        Returns:
            Ingestion result with saved path and index metadata.
        """
        try:
            if saved_path is None:
                saved_path = self.save_file()

            index_tool = IndexerTool(filepath=saved_path)
            index_result = index_tool._run()
            return {"saved_path": saved_path, "index_result": index_result}
        except (ValidationError, InternalError):
            raise
        except Exception as e:
            logger.exception("Ingestion/indexing failed: %s", e)
            raise InternalError("File ingestion failed") from e

