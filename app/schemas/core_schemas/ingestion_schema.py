from fastapi import UploadFile
from pydantic import BaseModel, Field, ConfigDict


class IngestionRequest(BaseModel):
    """Request body for file ingestion endpoint."""
    file: UploadFile = Field(..., description="File to upload")
    model_config = ConfigDict(arbitrary_types_allowed=True)

class IngestionResponse(BaseModel):
    """Response body for file ingestion endpoint."""
    message: str = Field(..., description="Upload status message")
    file_path: str = Field(..., description="Saved file path on server")
    filename: str = Field(..., description="Original filename")

