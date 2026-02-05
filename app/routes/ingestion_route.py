from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends

from app.config.log_config import logger
from app.services.ingestion_service import IngestionService
from app.schemas.ingestion_schema import IngestionResponse, IngestionRequest

router = APIRouter()

def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
    """Create an ingestion request from an uploaded file.

    Args:
        file: Uploaded file.

    Returns:
        IngestionRequest instance.
    """
    return IngestionRequest(file=file)

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
    """
    Upload a file, save it to the upload directory.

    Args:
        request: Ingestion request payload.

    Returns:
        Ingestion response payload.
    """
    try:
        file = request.file

        ingestion_service = IngestionService(file=file)
        ingest_result = ingestion_service.ingest_file()

        logger.info("Index result: %s", ingest_result["index_result"])
        
        response_dict = {
            "message": "File uploaded successfully",
            "file_path": ingest_result["saved_path"],
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
