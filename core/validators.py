import os
import logging
from pathlib import Path
from typing import Tuple, Optional
import config

logger = logging.getLogger(__name__)

class FileValidator:
    @staticmethod
    def validate_file_size(filepath: str, max_size: int = config.MAX_FILE_SIZE) -> Tuple[bool, Optional[str]]:
        try:
            size = os.path.getsize(filepath)
            if size > max_size:
                max_mb = max_size // (1024 * 1024)
                return False, f"File exceeds maximum size of {max_mb}MB"
            if size == 0:
                return False, "File is empty"
            return True, None
        except Exception as e:
            logger.error(f"Error validating file size: {e}")
            return False, "Could not validate file size"

    @staticmethod
    def validate_image_format(filepath: str) -> Tuple[bool, Optional[str]]:
        try:
            from PIL import Image
            with Image.open(filepath) as img:
                if img.format not in config.ALLOWED_IMAGE_FORMATS:
                    formats = ', '.join(config.ALLOWED_IMAGE_FORMATS)
                    return False, f"Unsupported format. Allowed: {formats}"
                return True, None
        except Exception as e:
            logger.error(f"Error validating image: {e}")
            return False, "Invalid or corrupted image file"

    @staticmethod
    def validate_video_extension(filename: str) -> Tuple[bool, Optional[str]]:
        ext = Path(filename).suffix.lower()
        if ext not in config.ALLOWED_VIDEO_EXTENSIONS:
            exts = ', '.join(config.ALLOWED_VIDEO_EXTENSIONS)
            return False, f"Unsupported video format. Allowed: {exts}"
        return True, None

    @staticmethod
    def validate_file_exists(filepath: str) -> Tuple[bool, Optional[str]]:
        if not os.path.exists(filepath):
            return False, "File does not exist"
        if not os.path.isfile(filepath):
            return False, "Path is not a file"
        if not os.access(filepath, os.R_OK):
            return False, "File is not readable"
        return True, None