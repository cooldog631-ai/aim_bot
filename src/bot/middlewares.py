"""Middleware for bot request processing."""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class AuthMiddleware(BaseMiddleware):
    """Middleware for user authentication and authorization."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """Check if user is allowed to use the bot."""
        settings = get_settings()

        if isinstance(event, Message):
            user_id = str(event.from_user.id)
            username = event.from_user.username or "unknown"

            # Check whitelist if configured
            allowed_users = settings.allowed_users_list
            if allowed_users and user_id not in allowed_users:
                logger.warning(f"Unauthorized access attempt from user {user_id} (@{username})")
                await event.answer(
                    "⛔️ У вас нет доступа к этому боту.\n"
                    "Обратитесь к администратору для получения разрешения."
                )
                return

            # Add user info to data
            data["user_id"] = user_id
            data["username"] = username
            data["is_admin"] = user_id in settings.admin_users_list

            logger.info(f"Request from user {user_id} (@{username})")

        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging all bot interactions."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """Log incoming events."""
        if isinstance(event, Message):
            content_type = event.content_type
            user = event.from_user
            logger.debug(
                f"Message from {user.id} (@{user.username}): "
                f"type={content_type}, text={event.text[:50] if event.text else 'N/A'}"
            )

        result = await handler(event, data)
        return result
