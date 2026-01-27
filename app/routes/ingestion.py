from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends

from app.config.logger import logger
from app.services.ingestion.ingestion_service import IngestionService
from app.schemas.ingestion import IngestionResponse, IngestionRequest

router = APIRouter()


def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
    return IngestionRequest(file=file)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
    """
    Upload a file, save it to the upload directory.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        dict: Message and the file path of the saved file.
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
