import os
import logging
import subprocess
from typing import Tuple, Optional
from PIL import Image
import config
from .validators import FileValidator

logger = logging.getLogger(__name__)


class MetadataRemover:
    def __init__(self):
        self.validator = FileValidator()

    def remove_image_metadata(
            self,
            input_path: str,
            output_path: str
    ) -> Tuple[bool, Optional[str]]:
        try:
            is_valid, error = self.validator.validate_file_exists(input_path)
            if not is_valid:
                return False, error

            is_valid, error = self.validator.validate_file_size(input_path)
            if not is_valid:
                return False, error

            is_valid, error = self.validator.validate_image_format(input_path)
            if not is_valid:
                return False, error

            image = Image.open(input_path)

            # Convert to RGB, removing any alpha channel metadata
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                if image.mode in ('RGBA', 'LA'):
                    background.paste(image, mask=image.split()[-1])
                else:
                    background.paste(image)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')

            # Create completely new image without any metadata
            # This ensures ALL hidden metadata is removed
            data = list(image.getdata())
            clean_image = Image.new('RGB', image.size)
            clean_image.putdata(data)

            # Save with explicit empty EXIF
            clean_image.save(
                output_path,
                format='JPEG',
                quality=95,
                optimize=True,
                exif=b''  # Explicitly empty EXIF data
            )

            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                return False, "Output file was not created properly"

            logger.info(f"Successfully removed metadata from image")
            return True, None

        except Exception as e:
            logger.error(f"Error removing image metadata: {e}")
            return False, f"Failed to process image: {str(e)}"

    def remove_video_metadata(
            self,
            input_path: str,
            output_path: str
    ) -> Tuple[bool, Optional[str]]:
        try:
            is_valid, error = self.validator.validate_file_exists(input_path)
            if not is_valid:
                return False, error

            is_valid, error = self.validator.validate_file_size(input_path)
            if not is_valid:
                return False, error

            try:
                subprocess.run(
                    ['ffmpeg', '-version'],
                    capture_output=True,
                    check=True,
                    timeout=5
                )
            except (subprocess.SubprocessError, FileNotFoundError):
                return False, "ffmpeg is not installed or not accessible"

            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-map_metadata', '-1',
                '-map_chapters', '-1',
                '-fflags', '+bitexact',
                '-flags:v', '+bitexact',
                '-flags:a', '+bitexact',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', config.VIDEO_ENCODING_PRESET,
                '-crf', str(config.VIDEO_QUALITY_CRF),
                '-movflags', '+faststart',
                '-y',
                str(output_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.VIDEO_PROCESSING_TIMEOUT,
                check=False
            )

            if result.returncode != 0:
                logger.error(f"ffmpeg error: {result.stderr}")
                return False, "Video processing failed"

            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                return False, "Output video was not created properly"

            logger.info(f"Successfully removed metadata from video")
            return True, None

        except subprocess.TimeoutExpired:
            logger.error("ffmpeg processing timeout")
            return False, f"Video processing timeout ({config.VIDEO_PROCESSING_TIMEOUT}s). Try a shorter video."
        except Exception as e:
            logger.error(f"Error removing video metadata: {e}")
            return False, f"Failed to process video: {str(e)}"