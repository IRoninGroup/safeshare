import logging
import sys
from clients.telegram_bot import TelegramBot
import config

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=getattr(logging, config.LOG_LEVEL)
)

logger = logging.getLogger(__name__)


def main():
    if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable or update config.py")
        sys.exit(1)

    bot = TelegramBot(config.TELEGRAM_BOT_TOKEN)
    bot.run()


if __name__ == '__main__':
    main()