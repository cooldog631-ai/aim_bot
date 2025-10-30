"""Admin handlers for bot management."""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router(name="admin")


@router.message(Command("admin"))
async def cmd_admin(message: Message, is_admin: bool = False):
    """Handle /admin command."""
    if not is_admin:
        await message.answer("⛔️ У вас нет прав администратора.")
        return

    admin_text = """
🔧 <b>Панель администратора</b>

Доступные команды:
/stats - Статистика по отчетам
/users - Список пользователей
/export - Экспорт данных
/logs - Просмотр логов

Функционал в разработке...
"""

    await message.answer(admin_text)


@router.message(Command("stats"))
async def cmd_stats(message: Message, is_admin: bool = False):
    """Handle /stats command."""
    if not is_admin:
        await message.answer("⛔️ Эта команда доступна только администраторам.")
        return

    # TODO: Implement statistics
    await message.answer("📊 Статистика пока в разработке...")


@router.message(Command("users"))
async def cmd_users(message: Message, is_admin: bool = False):
    """Handle /users command."""
    if not is_admin:
        await message.answer("⛔️ Эта команда доступна только администраторам.")
        return

    # TODO: Implement user list
    await message.answer("👥 Список пользователей пока в разработке...")


@router.message(Command("export"))
async def cmd_export(message: Message, is_admin: bool = False):
    """Handle /export command."""
    if not is_admin:
        await message.answer("⛔️ Эта команда доступна только администраторам.")
        return

    # TODO: Implement data export
    await message.answer("📤 Экспорт данных пока в разработке...")
