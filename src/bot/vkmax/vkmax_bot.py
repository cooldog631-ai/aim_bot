"""VK Max messenger bot implementation."""

import asyncio
from typing import Any, Callable, Optional

try:
    from maxapi import Bot, Dispatcher
    from maxapi.events import BotStarted, MessageCallback, MessageCreated
    from maxapi.filters import Command

    MAXAPI_AVAILABLE = True
except ImportError:
    MAXAPI_AVAILABLE = False
    Bot = None
    Dispatcher = None

from src.bot.base_messenger import BaseMessenger, MessageContext
from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class VKMaxBot(BaseMessenger):
    """VK Max messenger bot implementation."""

    def __init__(self):
        """Initialize VK Max bot."""
        if not MAXAPI_AVAILABLE:
            raise ImportError(
                "maxapi library not installed. Install with: pip install maxapi"
            )

        settings = get_settings()

        if not settings.vk_max_token:
            raise ValueError("VK_MAX_TOKEN not set in environment")

        # Initialize bot
        self.bot = Bot(settings.vk_max_token)
        self.dp = Dispatcher()

        # Handler storage
        self._handlers = []

        # Register built-in handlers
        self._register_builtin_handlers()

        logger.info("VK Max bot initialized")

    def _register_builtin_handlers(self):
        """Register built-in event handlers."""

        @self.dp.bot_started()
        async def on_bot_started(event: BotStarted):
            """Handle bot start event."""
            logger.info(f"Bot started with deep link: {event.payload}")

        @self.dp.message_created()
        async def on_message(event: MessageCreated):
            """Handle incoming messages."""
            try:
                # Convert to unified context
                context = self._create_context(event)

                # Call registered handlers
                for handler_info in self._handlers:
                    handler = handler_info["handler"]
                    content_types = handler_info["content_types"]
                    commands = handler_info.get("commands", [])

                    # Check if handler should process this message
                    should_process = False

                    # Check commands
                    if commands and context.text:
                        for cmd in commands:
                            if context.text.startswith(f"/{cmd}"):
                                should_process = True
                                break

                    # Check content types
                    if not should_process:
                        if "text" in content_types and context.is_text:
                            should_process = True
                        elif "voice" in content_types and context.is_voice:
                            should_process = True
                        elif "photo" in content_types and context.is_photo:
                            should_process = True

                    # Process message
                    if should_process:
                        await handler(context)

            except Exception as e:
                logger.error(f"Error handling message: {e}", exc_info=True)

    def _create_context(self, event: MessageCreated) -> MessageContext:
        """
        Create unified message context from VK Max event.

        Args:
            event: VK Max MessageCreated event

        Returns:
            MessageContext instance
        """
        message = event.message

        # Extract text
        text = message.text if hasattr(message, "text") else None

        # Extract voice file ID (from audio attachment with transcription)
        voice_file_id = None
        photo_file_id = None

        if hasattr(message, "attachments") and message.attachments:
            for attachment in message.attachments:
                # Check for audio (voice message)
                if attachment.type == "audio" and hasattr(attachment, "payload"):
                    voice_file_id = attachment.payload.token
                # Check for photo
                elif attachment.type == "photo" and hasattr(attachment, "payload"):
                    photo_file_id = attachment.payload.token

        return MessageContext(
            messenger=self,
            chat_id=str(event.chat_id),
            user_id=str(event.from_user.user_id) if hasattr(event, "from_user") else None,
            username=getattr(event.from_user, "username", None)
            if hasattr(event, "from_user")
            else None,
            message_id=str(message.message_id) if hasattr(message, "message_id") else None,
            text=text,
            voice_file_id=voice_file_id,
            photo_file_id=photo_file_id,
            raw_event=event,
        )

    async def start(self):
        """Start VK Max bot with polling."""
        logger.info("Starting VK Max bot...")
        try:
            # Start long polling
            await self.bot.start_polling(self.dp)
        except Exception as e:
            logger.error(f"Error starting VK Max bot: {e}", exc_info=True)
            raise

    async def stop(self):
        """Stop VK Max bot."""
        logger.info("Stopping VK Max bot...")
        # Cleanup if needed
        pass

    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: Optional[Any] = None,
        parse_mode: Optional[str] = None,
    ) -> Any:
        """
        Send text message to VK Max chat.

        Args:
            chat_id: Chat ID
            text: Message text
            reply_markup: Optional inline keyboard
            parse_mode: Optional text formatting

        Returns:
            Sent message info
        """
        try:
            # Prepare message params
            params = {"chat_id": chat_id, "text": text}

            # Add inline keyboard if provided
            if reply_markup:
                params["inline_keyboard_markup"] = reply_markup

            # VK Max doesn't support parse_mode directly like Telegram
            # Text formatting is done differently

            response = await self.bot.send_message(**params)
            return response

        except Exception as e:
            logger.error(f"Error sending message: {e}", exc_info=True)
            raise

    async def download_file(self, file_id: str) -> bytes:
        """
        Download file from VK Max.

        Args:
            file_id: File token from VK Max

        Returns:
            File content as bytes
        """
        try:
            # For audio/voice files
            # VK Max API provides file info through specific endpoints
            # This is a simplified implementation
            # You may need to use bot.get_file_info() or similar method

            # TODO: Implement actual file download from VK Max
            # For now, return empty bytes as placeholder
            logger.warning(f"File download not fully implemented for token: {file_id}")
            return b""

        except Exception as e:
            logger.error(f"Error downloading file: {e}", exc_info=True)
            raise

    async def upload_file(self, file_data: bytes, file_type: str) -> str:
        """
        Upload file to VK Max.

        Args:
            file_data: File content
            file_type: Type (audio, photo, file)

        Returns:
            File token for attaching
        """
        try:
            # VK Max upload process:
            # 1. Get upload URL from /uploads endpoint
            # 2. Upload file to that URL
            # 3. Receive token to attach to message

            # TODO: Implement actual file upload to VK Max
            logger.warning(f"File upload not fully implemented for type: {file_type}")
            return "placeholder_token"

        except Exception as e:
            logger.error(f"Error uploading file: {e}", exc_info=True)
            raise

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
        logger.debug(f"Registered handler for content types: {content_types}, commands: {commands}")

    @property
    def messenger_type(self) -> str:
        """Get messenger type identifier."""
        return "vkmax"
