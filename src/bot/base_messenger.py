"""Base messenger interface for unified bot interaction."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional


class BaseMessenger(ABC):
    """Abstract base class for messenger implementations."""

    @abstractmethod
    async def start(self):
        """Start the messenger bot."""
        pass

    @abstractmethod
    async def stop(self):
        """Stop the messenger bot and cleanup resources."""
        pass

    @abstractmethod
    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_markup: Optional[Any] = None,
        parse_mode: Optional[str] = None,
    ) -> Any:
        """
        Send text message to chat.

        Args:
            chat_id: Chat identifier
            text: Message text
            reply_markup: Optional inline keyboard
            parse_mode: Optional text formatting (HTML, Markdown)

        Returns:
            Message object
        """
        pass

    @abstractmethod
    async def download_file(self, file_id: str) -> bytes:
        """
        Download file by ID.

        Args:
            file_id: File identifier from messenger

        Returns:
            File content as bytes
        """
        pass

    @abstractmethod
    async def upload_file(self, file_data: bytes, file_type: str) -> str:
        """
        Upload file to messenger.

        Args:
            file_data: File content as bytes
            file_type: Type of file (photo, audio, document, etc.)

        Returns:
            File identifier for attaching to messages
        """
        pass

    @abstractmethod
    def register_message_handler(
        self, handler: Callable, content_types: list[str], commands: Optional[list[str]] = None
    ):
        """
        Register handler for incoming messages.

        Args:
            handler: Async function to handle messages
            content_types: List of content types (text, voice, photo, etc.)
            commands: Optional list of commands to handle
        """
        pass

    @property
    @abstractmethod
    def messenger_type(self) -> str:
        """Get messenger type identifier (telegram, vkmax, etc.)."""
        pass


class MessageContext:
    """Unified message context for handlers."""

    def __init__(
        self,
        messenger: BaseMessenger,
        chat_id: str,
        user_id: str,
        username: Optional[str] = None,
        message_id: Optional[str] = None,
        text: Optional[str] = None,
        voice_file_id: Optional[str] = None,
        photo_file_id: Optional[str] = None,
        raw_event: Optional[Any] = None,
    ):
        """
        Initialize message context.

        Args:
            messenger: Messenger instance
            chat_id: Chat identifier
            user_id: User identifier
            username: User username
            message_id: Message identifier
            text: Message text
            voice_file_id: Voice message file ID
            photo_file_id: Photo file ID
            raw_event: Raw event from messenger
        """
        self.messenger = messenger
        self.chat_id = chat_id
        self.user_id = user_id
        self.username = username
        self.message_id = message_id
        self.text = text
        self.voice_file_id = voice_file_id
        self.photo_file_id = photo_file_id
        self.raw_event = raw_event

    async def reply(self, text: str, reply_markup: Optional[Any] = None) -> Any:
        """Reply to this message."""
        return await self.messenger.send_message(
            chat_id=self.chat_id, text=text, reply_markup=reply_markup
        )

    async def download_voice(self) -> Optional[bytes]:
        """Download voice message if present."""
        if self.voice_file_id:
            return await self.messenger.download_file(self.voice_file_id)
        return None

    async def download_photo(self) -> Optional[bytes]:
        """Download photo if present."""
        if self.photo_file_id:
            return await self.messenger.download_file(self.photo_file_id)
        return None

    @property
    def is_voice(self) -> bool:
        """Check if message contains voice."""
        return self.voice_file_id is not None

    @property
    def is_photo(self) -> bool:
        """Check if message contains photo."""
        return self.photo_file_id is not None

    @property
    def is_text(self) -> bool:
        """Check if message contains text."""
        return self.text is not None and len(self.text.strip()) > 0
