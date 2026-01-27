from fastapi import APIRouter, UploadFile, File, status, HTTPException

from app.config.logger import logger
from app.services.file_processor import FileProcessor
from app.tools.indexing import IndexDocumentTool

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file, save it to the upload directory.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        dict: Message and the file path of the saved file.
    """
    try:
        # Save file
        ingestion_service = IngestionService(file=file)
        saved_path = ingestion_service.save_file()

        # Index the file
        index_result = ingestion_service.ingest(saved_path=saved_path)

        logger.info(f"Index result: {index_result}")
        
        response_dict = {
            "message": "File uploaded successfully",
            "file_path": saved_path,
            "filename": file.filename,
        }

        return response_dict

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(f"Unhandled error while uploading file: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File upload failed",
        )