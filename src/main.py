"""Main entry point for the AI Voice Reports Bot."""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Main application entry point."""
    settings = get_settings()

    logger.info("=" * 60)
    logger.info("🤖 AI Voice Reports Bot starting...")
    logger.info("=" * 60)
    logger.info(f"Version: 0.1.0")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"Database: {settings.database_url}")
    logger.info("=" * 60)

    # Import here to avoid circular imports
    from src.bot.telegram_bot import TelegramBot
    from src.database.session import init_db

    # Initialize database
    try:
        logger.info("📊 Initializing database...")
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

    # Start bot
    try:
        if not settings.telegram_bot_token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not set in .env file")
            logger.info("Please copy .env.example to .env and add your bot token")
            sys.exit(1)

        logger.info("🚀 Starting Telegram bot...")
        bot = TelegramBot()
        await bot.start()

    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
