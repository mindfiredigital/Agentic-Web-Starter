from fastapi import APIRouter, Depends, File, UploadFile, status

from app.config.log_config import logger
from app.schemas.ingestion_schema import IngestionRequest, IngestionResponse
from app.services.ingestion_service import IngestionService

router = APIRouter()

def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
    """Create an ingestion request from an uploaded file."""
    return IngestionRequest(file=file)

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
    """Upload a file and index it. Exceptions handled by global handlers."""
    file = request.file
    ingestion_service = IngestionService(file=file)
    ingest_result = ingestion_service.ingest_file()
    logger.info("Index result: %s", ingest_result["index_result"])
    return {
        "message": "File uploaded successfully",
        "file_path": ingest_result["saved_path"],
        "filename": file.filename,
    }
