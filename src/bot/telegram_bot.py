"""Main Telegram bot implementation."""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.handlers import admin, common, reports, voice
from src.bot.middlewares import AuthMiddleware, LoggingMiddleware
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramBot:
    """Telegram bot wrapper."""

    def __init__(self):
        """Initialize bot and dispatcher."""
        settings = get_settings()

        # Initialize bot with settings
        self.bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        # Initialize dispatcher with FSM storage
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)

        # Register middlewares
        self.dp.message.middleware(AuthMiddleware())
        self.dp.message.middleware(LoggingMiddleware())

        # Register handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all bot handlers."""
        # Order matters: specific handlers first, general handlers last
        self.dp.include_router(admin.router)
        self.dp.include_router(reports.router)
        self.dp.include_router(voice.router)
        self.dp.include_router(common.router)  # Common handlers last (catch-all)

    async def start(self):
        """Start the bot."""
        try:
            logger.info("🚀 Bot is starting...")

            # Delete webhook if exists (for polling mode)
            await self.bot.delete_webhook(drop_pending_updates=True)

            logger.info("✅ Bot started successfully!")
            logger.info("Listening for messages...")

            # Start polling
            await self.dp.start_polling(self.bot)

        except Exception as e:
            logger.error(f"Error starting bot: {e}", exc_info=True)
            raise
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up...")
        await self.bot.session.close()
        await self.storage.close()
