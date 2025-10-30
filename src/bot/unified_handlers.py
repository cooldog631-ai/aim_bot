"""Unified message handlers that work with any messenger."""

from src.bot.base_messenger import MessageContext
from src.bot.keyboards import get_main_menu_keyboard
from src.services.report_service import ReportService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize services
report_service = ReportService()


async def handle_start_command(context: MessageContext):
    """Handle /start command from any messenger."""
    user_name = context.username or "друг"

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

    # Note: VK Max doesn't support HTML formatting like Telegram
    # We'll send plain text
    if context.messenger.messenger_type == "vkmax":
        welcome_text = welcome_text.replace("<b>", "").replace("</b>", "")

    await context.reply(welcome_text)


async def handle_help_command(context: MessageContext):
    """Handle /help command from any messenger."""
    help_text = """
📚 <b>Доступные команды:</b>

/start - Начало работы
/help - Эта справка
/report - Отправить отчет
/my_reports - Мои отчеты за период
/cancel - Отменить текущую операцию

🎤 <b>Голосовые отчеты:</b>
Просто отправь голосовое сообщение с описанием работы.

📊 <b>Просмотр отчетов:</b>
Используй команду /my_reports

❓ <b>Нужна помощь?</b>
Обратись к администратору или отправь /start для начала работы.
"""

    if context.messenger.messenger_type == "vkmax":
        help_text = help_text.replace("<b>", "").replace("</b>", "")

    await context.reply(help_text)


async def handle_voice_message(context: MessageContext):
    """Handle voice messages from any messenger."""
    logger.info(f"Received voice message from user {context.user_id} via {context.messenger.messenger_type}")

    # Send processing message
    await context.reply("🎤 Получил голосовое сообщение, обрабатываю...")

    try:
        # Download voice file
        voice_data = await context.download_voice()

        if not voice_data:
            await context.reply("❌ Не удалось получить голосовое сообщение. Попробуй еще раз.")
            return

        # Process voice message through service
        result = await report_service.process_voice_message(context.user_id, voice_data)

        if result["status"] == "complete":
            # Report is complete, show for confirmation
            formatted_report = _format_report(result["data"])
            await context.reply(
                f"✅ Отчет обработан!\n\n{formatted_report}\n\n"
                f"Все верно? (Ответь 'да' для подтверждения или 'исправить' для изменений)"
            )

        elif result["status"] == "incomplete":
            # Need clarification
            questions = result.get("questions", "Пожалуйста, уточните недостающую информацию.")
            await context.reply(
                f"📝 Спасибо за отчет! Мне нужна еще пара деталей:\n\n{questions}\n\n"
                f"Ответь голосовым или текстовым сообщением."
            )

        else:
            # Error
            error_msg = result.get("error", "Неизвестная ошибка")
            await context.reply(f"❌ Произошла ошибка при обработке: {error_msg}\n\nПопробуй еще раз.")

    except Exception as e:
        logger.error(f"Error processing voice message: {e}", exc_info=True)
        await context.reply(
            "❌ Произошла ошибка при обработке голосового сообщения.\n\n"
            "Попробуй еще раз или обратись к администратору."
        )


async def handle_text_message(context: MessageContext):
    """Handle text messages from any messenger."""
    text = context.text.strip().lower()

    # Check for commands
    if text.startswith("/"):
        # Unknown command
        await context.reply(
            "🤔 Я не понял эту команду.\n\n"
            "Отправь голосовое сообщение для создания отчета или используй /help для справки."
        )
        return

    # Check for confirmation keywords
    if text in ["да", "yes", "подтвердить", "ok", "ок"]:
        await context.reply("✅ Отчет подтвержден!\n\nМожешь отправить следующий отчет.")
        # TODO: Save report to database
        return

    # General text message
    await context.reply(
        "📝 Получил текстовое сообщение.\n\n"
        "Для создания отчета отправь голосовое сообщение или используй /help для справки."
    )


def _format_report(data: dict) -> str:
    """Format report data for display."""
    return f"""
📅 Дата: {data.get('date', 'N/A')}
🚜 Техника: {data.get('equipment_number', 'N/A')}
👷 Бригада: {data.get('brigade_number', 'N/A')}
📝 Выполненные работы:
{data.get('work_description', 'N/A')}
""".strip()
