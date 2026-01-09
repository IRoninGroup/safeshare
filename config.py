import os

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG', 'WEBP'}
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv'}

# if you want to use telegram bot as your client if not leave it empty
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

TEMP_DIR_PREFIX = 'safesend_'
SECURE_DELETE_ENABLED = True

VIDEO_ENCODING_PRESET = 'medium'
VIDEO_QUALITY_CRF = 23  # Lower = better quality (18-28 recommended)
VIDEO_PROCESSING_TIMEOUT = 300  # 5 minutes

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'