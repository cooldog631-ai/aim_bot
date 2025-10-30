"""Handler for voice messages."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import get_confirmation_keyboard
from src.bot.states import ReportStates
from src.services.report_service import ReportService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router(name="voice")

# Initialize service
report_service = ReportService()


@router.message(F.voice)
async def handle_voice_message(message: Message, state: FSMContext, user_id: str):
    """Handle incoming voice messages."""
    logger.info(f"Received voice message from user {user_id}")

    # Send processing message
    processing_msg = await message.answer("🎤 Получил голосовое сообщение, обрабатываю...")

    try:
        # Download voice file
        voice_file = await message.bot.download(message.voice.file_id)

        # Read file content
        voice_data = voice_file.read()

        # Process voice message through service
        result = await report_service.process_voice_message(user_id, voice_data)

        # Delete processing message
        await processing_msg.delete()

        if result["status"] == "complete":
            # Report is complete, show for confirmation
            formatted_report = _format_report(result["data"])
            await message.answer(
                f"✅ <b>Отчет обработан!</b>\n\n{formatted_report}\n\n"
                f"Все верно? Подтвердите или запросите исправления.",
                reply_markup=get_confirmation_keyboard(),
            )
            await state.set_state(ReportStates.waiting_for_confirmation)
            await state.update_data(report_data=result["data"])

        elif result["status"] == "incomplete":
            # Need clarification
            missing_fields = result.get("missing_fields", [])
            questions = result.get("questions", "Пожалуйста, уточните недостающую информацию.")

            await message.answer(
                f"📝 Спасибо за отчет! Мне нужна еще пара деталей:\n\n{questions}\n\n"
                f"Ответь голосовым или текстовым сообщением."
            )
            await state.set_state(ReportStates.waiting_for_clarification)
            await state.update_data(
                partial_data=result.get("data", {}), missing_fields=missing_fields
            )

        else:
            # Error
            error_msg = result.get("error", "Неизвестная ошибка")
            await message.answer(f"❌ Произошла ошибка при обработке: {error_msg}\n\nПопробуй еще раз.")

    except Exception as e:
        logger.error(f"Error processing voice message: {e}", exc_info=True)
        await processing_msg.delete()
        await message.answer(
            "❌ Произошла ошибка при обработке голосового сообщения.\n\n"
            "Попробуй еще раз или обратись к администратору."
        )


@router.message(ReportStates.waiting_for_clarification, F.text | F.voice)
async def handle_clarification(message: Message, state: FSMContext, user_id: str):
    """Handle clarification messages (text or voice)."""
    data = await state.get_data()
    partial_data = data.get("partial_data", {})

    processing_msg = await message.answer("🔄 Обрабатываю дополнительную информацию...")

    try:
        if message.voice:
            # Download and process voice
            voice_file = await message.bot.download(message.voice.file_id)
            voice_data = voice_file.read()
            result = await report_service.process_clarification(
                user_id, voice_data, partial_data, is_voice=True
            )
        else:
            # Process text
            result = await report_service.process_clarification(
                user_id, message.text, partial_data, is_voice=False
            )

        await processing_msg.delete()

        if result["status"] == "complete":
            formatted_report = _format_report(result["data"])
            await message.answer(
                f"✅ <b>Отлично! Все данные собраны.</b>\n\n{formatted_report}\n\n"
                f"Все верно? Подтвердите или запросите исправления.",
                reply_markup=get_confirmation_keyboard(),
            )
            await state.set_state(ReportStates.waiting_for_confirmation)
            await state.update_data(report_data=result["data"])

        elif result["status"] == "incomplete":
            questions = result.get("questions", "Пожалуйста, уточните недостающую информацию.")
            await message.answer(f"📝 {questions}")
            await state.update_data(partial_data=result.get("data", {}))

    except Exception as e:
        logger.error(f"Error processing clarification: {e}", exc_info=True)
        await processing_msg.delete()
        await message.answer("❌ Ошибка обработки. Попробуй еще раз.")


def _format_report(data: dict) -> str:
    """Format report data for display."""
    return f"""
📅 <b>Дата:</b> {data.get('date', 'N/A')}
🚜 <b>Техника:</b> {data.get('equipment_number', 'N/A')}
👷 <b>Бригада:</b> {data.get('brigade_number', 'N/A')}
📝 <b>Выполненные работы:</b>
{data.get('work_description', 'N/A')}
""".strip()
