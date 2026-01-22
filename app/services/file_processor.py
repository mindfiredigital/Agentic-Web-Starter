import os 
from app.constants.app_constants import Environment, ALLOWED_FILES
from app.config.logger import logger
import shutil
from fastapi import UploadFile, HTTPException


class FileProcessor:
    def __init__(self, file: UploadFile):
        self.file = file

    def get_file_name(self)->str:
        """
        Get the file name.
        """
        return self.file.filename

    def get_file_extension(self)->str:
        """
        Get the file extension.
        """
        return os.path.splitext(self.file.filename)[1].lower()

    def get_file_size(self)->int:
        """
        Get the file size.
        """
        return os.path.getsize(self.file.filename)

    def get_file_path(self)->str:
        file_name = self.get_file_name()
        file_extension = self.get_file_extension()

        if not any(file_extension == ext.lower() for ext in ALLOWED_FILES.ALL_FILES.value):
            logger.error(f"Invalid file extension: {file_extension}")
            raise HTTPException(status_code=400, detail="Invalid file extension")
    
        try:
            if not os.path.exists(Environment.UPLOAD_DIR.value):
                os.makedirs(Environment.UPLOAD_DIR.value)

            file_path = os.path.join(Environment.UPLOAD_DIR.value, file_name)
            logger.info(f"File path: {file_path}")

        except Exception as e:
            logger.error(f"Error creating upload directory: {e}")
            raise HTTPException(status_code=500, detail="Error creating upload directory")

        return file_path

    def save_file(self, file_path: str):
        """
        Save the file to the file path.
        """
        with open(file_path, "wb") as f:
            shutil.copyfileobj(self.file.file, f)
        logger.info(f"File saved to: {file_path}")
        return file_path

    def delete_file(self, file_path: str):
        """
        Delete the file from the file path.
        """
        os.remove(file_path)
        logger.info(f"File deleted: {file_path}")
        return file_path


    