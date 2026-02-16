from typing import Any, Dict, Optional

from fastapi import UploadFile

from app.config.log_config import logger
from app.exceptions import InternalError, ValidationError
from app.tools.indexer_tool import IndexerTool
from app.utils.core_utils.document import FileProcessor


class IngestionService:
    """Stateless service for file storage and indexing. Use the module-level instance."""

    def save_file(self, file: UploadFile) -> str:
        """Save the file to the upload directory.

        Args:
            file: The uploaded file to save.

        Returns:
            Saved file path.
        """
        try:
            file_processor = FileProcessor(file=file)
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

    def ingest_file(
        self, file: UploadFile, saved_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Save the file (if needed) and index it into the vector database.

        Args:
            file: The uploaded file.
            saved_path: Optional pre-saved file path; if None, file is saved first.

        Returns:
            Ingestion result with saved path and index metadata.
        """
        try:
            if saved_path is None:
                saved_path = self.save_file(file)

            index_result = self.index_file(saved_path)
            return {"saved_path": saved_path, "index_result": index_result}
        except (ValidationError, InternalError):
            raise
        except Exception as e:
            logger.exception("Ingestion/indexing failed: %s", e)
            raise InternalError("File ingestion failed") from e

    def index_file(self, filepath: str) -> Any:
        """Index an already-saved file into the vector database (e.g. for workers).

        Args:
            filepath: Path to the saved file.

        Returns:
            Index tool result.
        """
        try:
            index_tool = IndexerTool(filepath=filepath)
            return index_tool._run()
        except Exception as e:
            logger.exception("Indexing failed for filepath=%s: %s", filepath, e)
            raise InternalError("File ingestion failed") from e


# Singleton instance for use when USE_QDRANT (or other env) enables ingestion.
ingestion_service = IngestionService()

