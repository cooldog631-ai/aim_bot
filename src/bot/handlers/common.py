"""Common bot handlers for /start, /help and other basic commands."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.bot.keyboards import get_main_menu_keyboard
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    user_name = message.from_user.first_name or "друг"

    welcome_text = f"""
👋 Привет, <b>{user_name}</b>!

Я - AI Voice Reports Bot, помогу тебе быстро отправлять отчеты голосом.

🎤 <b>Как это работает:</b>
1. Запиши голосовое сообщение с отчетом
2. Я транскрибирую его и проверю на полноту
3. Если чего-то не хватает - попрошу уточнить
4. Ты подтверждаешь - я сохраняю в базу

📝 <b>Обязательные данные в отчете:</b>
• Дата работы
• Номер техники/комбайна
• Номер бригады
• Описание выполненных работ

Используй команду /help для справки по всем командам.
"""

    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = """
📚 <b>Доступные команды:</b>

/start - Начало работы
/help - Эта справка
/report - Отправить отчет
/my_reports - Мои отчеты за период
/edit_last - Исправить последний отчет
/cancel - Отменить текущую операцию

🎤 <b>Голосовые отчеты:</b>
Просто отправь голосовое сообщение с описанием работы.

📊 <b>Просмотр отчетов:</b>
Используй кнопки меню или команду /my_reports

❓ <b>Нужна помощь?</b>
Обратись к администратору или отправь /start для начала работы.
"""

    await message.answer(help_text)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    """Handle /cancel command."""
    await message.answer(
        "❌ Текущая операция отменена.\n\n" "Используй /start для начала работы.",
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(lambda message: message.text in ["❓ Помощь", "Помощь"])
async def menu_help(message: Message):
    """Handle help button from menu."""
    await cmd_help(message)


@router.message()
async def handle_unknown(message: Message):
    """Handle unknown messages."""
    await message.answer(
        "🤔 Я не понял эту команду.\n\n"
        "Отправь голосовое сообщение для создания отчета или используй /help для справки."
    )
