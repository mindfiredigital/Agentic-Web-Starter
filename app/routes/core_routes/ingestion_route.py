from fastapi import APIRouter, Depends, File, UploadFile, status

from app.config.env_config import settings
from app.config.log_config import logger
from app.services.core_services.ingestion_service import IngestionService
from app.schemas.core_schemas.ingestion_schema import IngestionRequest, IngestionResponse
from app.services.message_queue_services.message_queue_client import MessageQueueClient

router = APIRouter()


def get_ingestion_request(file: UploadFile = File(...)) -> IngestionRequest:
    """Create an ingestion request from an uploaded file.

    Args:
        file: File uploaded via multipart form.

    Returns:
        IngestionRequest wrapping the file.
    """
    return IngestionRequest(file=file)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=IngestionResponse)
async def ingest_file(request: IngestionRequest = Depends(get_ingestion_request)):
    """Upload a file and index it (or queue for async ingestion if RabbitMQ enabled).

    Args:
        request: IngestionRequest with uploaded file.

    Returns:
        IngestionResponse with message, file_path, and filename.

    Exceptions handled by global handlers.
    """
    file = request.file
    ingestion_service = IngestionService(file=file)
    if settings.USE_RABBITMQ:
        saved_path = ingestion_service.save_file()
        client = MessageQueueClient()
        await client.publish_json(
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

