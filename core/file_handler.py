import os
import logging
import secrets
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional
import config

logger = logging.getLogger(__name__)

class SecureFileHandler:
    def __init__(self, temp_dir: Optional[str] = None):
        if temp_dir:
            self.temp_dir = Path(temp_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.temp_dir = Path(tempfile.mkdtemp(prefix=config.TEMP_DIR_PREFIX))

        logger.info(f"Initialized SecureFileHandler with temp_dir: {self.temp_dir}")

    def generate_secure_filename(self, extension: str = '') -> str:
        random_name = secrets.token_hex(16)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{random_name}{extension}"

    def get_temp_path(self, extension: str = '') -> Path:
        filename = self.generate_secure_filename(extension)
        return self.temp_dir / filename

    def cleanup_file(self, filepath: Optional[Path]) -> None:
        if not filepath:
            return

        try:
            filepath = Path(filepath)
            if not filepath.exists():
                return

            if config.SECURE_DELETE_ENABLED:
                file_size = filepath.stat().st_size
                if file_size < 10 * 1024 * 1024:
                    try:
                        with open(filepath, 'ba+') as f:
                            f.seek(0)
                            f.write(os.urandom(file_size))
                    except Exception as e:
                        logger.warning(f"Could not overwrite file before deletion: {e}")

            filepath.unlink()
            logger.debug(f"Cleaned up file: {filepath.name}")

        except Exception as e:
            logger.error(f"Error cleaning up file {filepath}: {e}")

    def cleanup_directory(self) -> None:
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_directory()

