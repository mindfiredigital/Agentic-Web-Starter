from fastapi import APIRouter, UploadFile, File, status, HTTPException

from app.config.logger import logger
from app.services.file_processor import FileProcessor

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
        # Initialize file processor with the uploaded file
        file_processor = FileProcessor(file)

        # Get file path
        file_path = file_processor.get_file_path()

        # Save file
        file_path = file_processor.save_file(file_path)

        logger.info(f"File uploaded successfully saved at: {file_path}")

        response_dict = {
            "message": "File uploaded successfully",
            "file_path": file_path,
            "filename": file.filename,
        }
        logger.info(f"Response dictionary: {response_dict}")

        return response_dict
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception(f"Unhandled error while uploading file: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File upload failed",
        )