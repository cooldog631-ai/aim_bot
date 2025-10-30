"""Messenger manager to handle multiple messenger platforms."""

import asyncio
from typing import List, Optional

from src.bot.base_messenger import BaseMessenger
from src.bot.telegram_bot_adapter import TelegramBotAdapter
from src.bot.unified_handlers import (
    handle_help_command,
    handle_start_command,
    handle_text_message,
    handle_voice_message,
)
from src.bot.vkmax.vkmax_bot import VKMaxBot
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MessengerManager:
    """Manager for multiple messenger platforms."""

    def __init__(self):
        """Initialize messenger manager."""
        self.messengers: List[BaseMessenger] = []
        self.settings = get_settings()

    def _create_messengers(self) -> List[BaseMessenger]:
        """
        Create messenger instances based on configuration.

        Returns:
            List of messenger instances
        """
        messengers = []

        if self.settings.messenger_type in ["telegram", "both"]:
            if self.settings.telegram_bot_token:
                try:
                    logger.info("Initializing Telegram bot...")
                    telegram_bot = TelegramBotAdapter()
                    messengers.append(telegram_bot)
                    logger.info("✅ Telegram bot initialized")
                except Exception as e:
                    logger.error(f"Failed to initialize Telegram bot: {e}")
            else:
                logger.warning("TELEGRAM_BOT_TOKEN not set, skipping Telegram bot")

        if self.settings.messenger_type in ["vkmax", "both"]:
            if self.settings.vk_max_token:
                try:
                    logger.info("Initializing VK Max bot...")
                    vkmax_bot = VKMaxBot()
                    messengers.append(vkmax_bot)
                    logger.info("✅ VK Max bot initialized")
                except ImportError as e:
                    logger.error(
                        f"Failed to initialize VK Max bot: {e}\n"
                        f"Install maxapi: pip install maxapi"
                    )
                except Exception as e:
                    logger.error(f"Failed to initialize VK Max bot: {e}")
            else:
                logger.warning("VK_MAX_TOKEN not set, skipping VK Max bot")

        if not messengers:
            raise ValueError(
                "No messengers configured. Please set TELEGRAM_BOT_TOKEN or VK_MAX_TOKEN in .env"
            )

        return messengers

    def _register_unified_handlers(self, messenger: BaseMessenger):
        """
        Register unified handlers for a messenger.

        Args:
            messenger: Messenger instance to register handlers for
        """
        logger.info(f"Registering handlers for {messenger.messenger_type}...")

        # Register /start command
        messenger.register_message_handler(
            handler=handle_start_command, content_types=["text"], commands=["start"]
        )

        # Register /help command
        messenger.register_message_handler(
            handler=handle_help_command, content_types=["text"], commands=["help"]
        )

        # Register voice message handler
        messenger.register_message_handler(
            handler=handle_voice_message, content_types=["voice"]
        )

        # Register text message handler (for general text)
        messenger.register_message_handler(
            handler=handle_text_message, content_types=["text"]
        )

        logger.info(f"✅ Handlers registered for {messenger.messenger_type}")

    async def start(self):
        """Start all configured messengers."""
        logger.info("=" * 60)
        logger.info("🚀 Starting AI Voice Reports Bot...")
        logger.info("=" * 60)
        logger.info(f"Messenger type: {self.settings.messenger_type}")
        logger.info(f"LLM Provider: {self.settings.llm_provider}")
        logger.info(f"Database: {self.settings.database_url}")
        logger.info("=" * 60)

        # Create messengers
        self.messengers = self._create_messengers()

        logger.info(f"Initialized {len(self.messengers)} messenger(s):")
        for messenger in self.messengers:
            logger.info(f"  - {messenger.messenger_type}")

        # Register handlers for each messenger
        for messenger in self.messengers:
            self._register_unified_handlers(messenger)

        # Start all messengers concurrently
        logger.info("\n🚀 Starting all messengers...")

        if len(self.messengers) == 1:
            # Single messenger - just run it
            await self.messengers[0].start()
        else:
            # Multiple messengers - run concurrently
            tasks = [messenger.start() for messenger in self.messengers]
            await asyncio.gather(*tasks)

    async def stop(self):
        """Stop all messengers."""
        logger.info("Stopping all messengers...")

        stop_tasks = [messenger.stop() for messenger in self.messengers]
        await asyncio.gather(*stop_tasks, return_exceptions=True)

        logger.info("All messengers stopped")
