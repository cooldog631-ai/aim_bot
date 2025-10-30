"""Telegram bot implementation with BaseMessenger interface."""

from typing import Any, Callable, Optional

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from src.bot.base_messenger import BaseMessenger, MessageContext
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TelegramBotAdapter(BaseMessenger):
    """Telegram bot implementation following BaseMessenger interface."""

    def __init__(self):
        """Initialize Telegram bot."""
        settings = get_settings()

        if not settings.telegram_bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")

        # Initialize bot
        self.bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        # Initialize dispatcher
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)

        # Handler storage
        self._handlers = []

        # Register built-in message router
        self._register_message_router()

        logger.info("Telegram bot initialized")

    def _register_message_router(self):
        """Register message router that calls registered handlers."""

        @self.dp.message()
        async def handle_all_messages(message: Message):
            """Handle all incoming messages."""
            try:
                # Convert to unified context
                context = self._create_context(message)

                # Call registered handlers
                for handler_info in self._handlers:
                    handler = handler_info["handler"]
                    content_types = handler_info["content_types"]
                    commands = handler_info.get("commands", [])

                    # Check if handler should process this message
                    should_process = False

                    # Check commands
                    if commands and message.text:
                        for cmd in commands:
                            if message.text.startswith(f"/{cmd}"):
                                should_process = True
                                break

                    # Check content types
                    if not should_process:
                        if "text" in content_types and message.text and not message.text.startswith("/"):
                            should_process = True
                        elif "voice" in content_types and message.voice:
                            should_process = True
                        elif "photo" in content_types and message.photo:
                            should_process = True

                    # Process message
                    if should_process:
                        await handler(context)
                        # Don't break - allow multiple handlers if needed

            except Exception as e:
                logger.error(f"Error handling message: {e}", exc_info=True)

    def _create_context(self, message: Message) -> MessageContext:
        """
        Create unified message context from Telegram message.

        Args:
            message: Telegram message

        Returns:
            MessageContext instance
        """
        # Extract voice file ID
        voice_file_id = message.voice.file_id if message.voice else None

        # Extract photo file ID (largest size)
        photo_file_id = None
        if message.photo:
            photo_file_id = message.photo[-1].file_id

        return MessageContext(
            messenger=self,
            chat_id=str(message.chat.id),
            user_id=str(message.from_user.id),
            username=message.from_user.username,
            message_id=str(message.message_id),
            text=message.text,
            voice_file_id=voice_file_id,
            photo_file_id=photo_file_id,
            raw_event=message,
        )

    async def start(self):
        """Start Telegram bot with polling."""
        logger.info("Starting Telegram bot...")
        try:
            # Delete webhook if exists (for polling mode)
            await self.bot.delete_webhook(drop_pending_updates=True)

            logger.info("✅ Telegram bot started!")
            logger.info("Listening for messages...")

            # Start polling
            await self.dp.start_polling(self.bot)

        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}", exc_info=True)
            raise
        finally:
            await self.cleanup()

    async def stop(self):
        """Stop Telegram bot."""
        logger.info("Stopping Telegram bot...")
        await self.cleanup()

    async def cleanup(self):
        """Cleanup resources."""
        logger.info("🧹 Cleaning up Telegram bot...")
        await self.bot.session.close()
        await self.storage.close()

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: Optional[Any] = None,
        parse_mode: Optional[str] = None,
    ) -> Any:
        """
        Send text message to Telegram chat.

        Args:
            chat_id: Chat ID
            text: Message text
            reply_markup: Optional inline keyboard
            parse_mode: Optional parse mode (HTML, Markdown)

        Returns:
            Sent message
        """
        try:
            return await self.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode or ParseMode.HTML,
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}", exc_info=True)
            raise

    async def download_file(self, file_id: str) -> bytes:
        """
        Download file from Telegram.

        Args:
            file_id: Telegram file ID

        Returns:
            File content as bytes
        """
        try:
            # Get file info
            file = await self.bot.get_file(file_id)

            # Download file
            file_data = await self.bot.download_file(file.file_path)

            # Read bytes
            return file_data.read()

        except Exception as e:
            logger.error(f"Error downloading file: {e}", exc_info=True)
            raise

    async def upload_file(self, file_data: bytes, file_type: str) -> str:
        """
        Upload file to Telegram (not really needed, just send directly).

        Args:
            file_data: File content
            file_type: Type (audio, photo, document)

        Returns:
            File identifier (in Telegram we don't pre-upload)
        """
        # Telegram doesn't require pre-upload like VK Max
        # Files are sent directly with messages
        logger.warning("Telegram doesn't require file pre-upload")
        return "telegram_direct_upload"

    def register_message_handler(
        self, handler: Callable, content_types: list[str], commands: Optional[list[str]] = None
    ):
        """
        Register message handler.

        Args:
            handler: Async function to handle messages
            content_types: List of content types (text, voice, photo)
            commands: Optional list of commands
        """
        self._handlers.append(
            {"handler": handler, "content_types": content_types, "commands": commands or []}
        )
        logger.debug(
            f"Registered Telegram handler for content types: {content_types}, commands: {commands}"
        )

    @property
    def messenger_type(self) -> str:
        """Get messenger type identifier."""
        return "telegram"
