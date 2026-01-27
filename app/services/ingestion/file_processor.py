import os 
from app.constants.app_constants import Environment, ALLOWED_FILES
from app.config.log_config import logger
import shutil
from fastapi import UploadFile, HTTPException


class FileProcessor:
    """Handle file validation and storage operations."""

    def __init__(self, file: UploadFile):
        self.file = file

    def get_file_name(self)->str:
        """Return the uploaded file name.

        Returns:
            Filename string.
        """
        return self.file.filename

    def get_file_extension(self)->str:
        """Return the uploaded file extension.

        Returns:
            File extension string.
        """
        return os.path.splitext(self.file.filename)[1].lower()

    def get_file_size(self)->int:
        """Return the uploaded file size.

        Returns:
            File size in bytes.
        """
        return os.path.getsize(self.file.filename)

    def get_file_path(self)->str:
        """Build a validated destination path for the upload.

        Returns:
            Full file path string.

        Raises:
            HTTPException: If extension is invalid or upload dir is missing.
        """
        file_name = self.get_file_name()
        file_extension = self.get_file_extension()

        if not any(file_extension == ext.lower() for ext in ALLOWED_FILES.ALL_FILES.value):
            logger.error(f"Invalid file extension: {file_extension}")
            raise HTTPException(status_code=400, detail="Invalid file extension")
    
        if not os.path.exists(Environment.UPLOAD_DIR.value):
            logger.error("Upload directory not found: %s", Environment.UPLOAD_DIR.value)
            raise HTTPException(status_code=500, detail="Upload directory is missing")

        file_path = os.path.join(Environment.UPLOAD_DIR.value, file_name)
        logger.info(f"File path: {file_path}")

        return file_path

    def save_file(self, file_path: str):
        """Save the file to disk.

        Args:
            file_path: Destination path for the file.

        Returns:
            Path where the file was saved.
        """
        with open(file_path, "wb") as f:
            shutil.copyfileobj(self.file.file, f)
        logger.info(f"File saved to: {file_path}")
        return file_path

    def delete_file(self, file_path: str):
        """Delete the file at the given path.

        Args:
            file_path: Path to the file to delete.

        Returns:
            Deleted file path.
        """
        os.remove(file_path)
        logger.info(f"File deleted: {file_path}")
        return file_path


    