import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from core import MetadataRemover, SecureFileHandler, FileValidator
import config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.metadata_remover = MetadataRemover()
        self.file_handler = SecureFileHandler()
        self.validator = FileValidator()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_message = (
            "🔒 *SafeSend - Metadata Removal Bot*\n\n"
            "Send me photos or videos and I'll remove all metadata to protect your privacy.\n\n"
            "⚠️ *What metadata is removed:*\n"
            "• GPS location data\n"
            "• Device information (camera, phone model)\n"
            "• Timestamps (when photo/video was taken)\n"
            "• Camera settings (ISO, aperture, etc.)\n"
            "• Software information\n"
            "• Thumbnail images\n\n"
            "📋 *Limits:*\n"
            f"• Max file size: {config.MAX_FILE_SIZE // (1024 * 1024)}MB\n"
            f"• Images: {', '.join(config.ALLOWED_IMAGE_FORMATS)}\n"
            f"• Videos: {', '.join(config.ALLOWED_VIDEO_EXTENSIONS)}\n\n"
            "🔐 *Privacy:*\n"
            "• Files are processed and deleted immediately\n"
            "• No logs of your media are kept\n"
            "• Use /help for security tips"
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "📖 *How to use:*\n\n"
            "1. Send me a photo or video\n"
            "2. I'll remove all metadata\n"
            "3. You'll receive the cleaned file\n\n"
            "⚠️ *Critical Security Tips:*\n\n"
            "*Before taking photos/videos:*\n"
            "• Turn OFF location services\n"
            "• Use airplane mode if possible\n"
            "• Remove SIM card for maximum safety\n\n"
            "*Additional protection:*\n"
            "• Use a VPN or Tor\n"
            "• Avoid identifiable landmarks\n"
            "• Check reflections in windows/mirrors\n"
            "• Don't include faces without consent\n"
            "• Remove distinctive clothing/items\n"
            "• Be aware of background sounds in videos\n\n"
            "*After cleaning:*\n"
            "• Verify metadata is removed\n"
            "• Share through encrypted channels\n\n"
            "⚡ *Remember:* This removes metadata, but visual content can still identify locations/people!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        logger.info(f"Photo received from user {user_id}")

        await update.message.reply_text("📸 Processing your photo securely...")

        photo = update.message.photo[-1]
        input_path = None
        output_path = None

        try:
            if photo.file_size and photo.file_size > config.MAX_FILE_SIZE:
                await update.message.reply_text(
                    f"❌ File too large. Maximum size is {config.MAX_FILE_SIZE // (1024 * 1024)}MB"
                )
                return

            file = await context.bot.get_file(photo.file_id)
            input_path = self.file_handler.get_temp_path('.jpg')
            await file.download_to_drive(input_path)

            # Process image
            output_path = self.file_handler.get_temp_path('.jpg')
            success, error = self.metadata_remover.remove_image_metadata(
                str(input_path),
                str(output_path)
            )

            if success:
                with open(output_path, 'rb') as f:
                    await update.message.reply_photo(
                        photo=f,
                        caption=(
                            "✅ *Metadata removed!*\n\n"
                            "⚠️ Remember:\n"
                            "• Verify with a metadata viewer\n"
                            "• Visual content may still identify you\n"
                            "• Use additional security measures"
                        ),
                        parse_mode='Markdown'
                    )
                logger.info(f"Successfully processed photo for user {user_id}")
            else:
                await update.message.reply_text(f"❌ {error}")

        except Exception as e:
            logger.error(f"Error handling photo: {e}")
            await update.message.reply_text("❌ An error occurred. Please try again.")

        finally:
            self.file_handler.cleanup_file(input_path)
            self.file_handler.cleanup_file(output_path)

    async def handle_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        logger.info(f"Video received from user {user_id}")

        await update.message.reply_text(
            "🎥 Processing your video securely...\n"
            "⏳ This may take several minutes."
        )

        video = update.message.video
        input_path = None
        output_path = None

        try:
            if video.file_size > config.MAX_FILE_SIZE:
                await update.message.reply_text(
                    f"❌ File too large. Maximum size is {config.MAX_FILE_SIZE // (1024 * 1024)}MB"
                )
                return

            file = await context.bot.get_file(video.file_id)
            input_path = self.file_handler.get_temp_path('.mp4')
            await file.download_to_drive(input_path)

            output_path = self.file_handler.get_temp_path('.mp4')
            success, error = self.metadata_remover.remove_video_metadata(
                str(input_path),
                str(output_path)
            )

            if success:
                with open(output_path, 'rb') as f:
                    await update.message.reply_video(
                        video=f,
                        caption=(
                            "✅ *Metadata removed!*\n\n"
                            "⚠️ Video/audio content may still identify you!"
                        ),
                        parse_mode='Markdown'
                    )
                # logger.info(f"Successfully processed video for user {user_id}")
            else:
                await update.message.reply_text(f"❌ {error}")

        except Exception as e:
            logger.error(f"Error handling video: {e}")
            await update.message.reply_text("❌ An error occurred. Try a shorter video.")

        finally:
            self.file_handler.cleanup_file(input_path)
            self.file_handler.cleanup_file(output_path)

    def run(self):
        try:
            application = Application.builder().token(self.token).build()

            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
            application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))

            logger.info("Telegram bot starting...")
            application.run_polling(allowed_updates=Update.ALL_TYPES)

        finally:
            self.file_handler.cleanup_directory()

