from fastapi import UploadFile
from pydantic import BaseModel, Field


class UploadRequest(BaseModel):
    file: UploadFile = Field(..., description="File to upload")

    class Config:
        arbitrary_types_allowed = True


class UploadResponse(BaseModel):
    message: str = Field(..., description="Upload status message")
    file_path: str = Field(..., description="Saved file path on server")
    filename: str = Field(..., description="Original filename")
