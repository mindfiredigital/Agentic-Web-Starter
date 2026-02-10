from fastapi import APIRouter, Depends, File, UploadFile, status

from app.config.env_config import settings
from app.config.log_config import logger
from app.services.core_services.ingestion_service import IngestionService
from app.schemas.core_schemas.ingestion_schema import IngestionRequest, IngestionResponse
from app.utils.core_utils.queue.rabbitmq_utils import publish_json

router = APIRouter()


def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
    """Create an ingestion request from an uploaded file."""
    return IngestionRequest(file=file)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
    """Upload a file and index it. Exceptions handled by global handlers."""
    file = request.file
    ingestion_service = IngestionService(file=file)
    if settings.USE_RABBITMQ_INGESTION:
        saved_path = ingestion_service.save_file()
        await publish_json(
            settings.RABBITMQ_INGEST_QUEUE,
            {"saved_path": saved_path, "filename": file.filename},
        )
        return {
            "message": "File uploaded successfully (ingestion queued)",
            "file_path": saved_path,
            "filename": file.filename,
        }

    ingest_result = ingestion_service.ingest_file()
    logger.info("Index result: %s", ingest_result["index_result"])
    return {
        "message": "File uploaded successfully",
        "file_path": ingest_result["saved_path"],
        "filename": file.filename,
    }

