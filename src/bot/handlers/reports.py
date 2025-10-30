"""Handlers for report-related commands."""

from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.keyboards import get_main_menu_keyboard, get_period_keyboard
from src.bot.states import ReportStates
from src.services.report_service import ReportService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = Router(name="reports")

# Initialize service
report_service = ReportService()


@router.message(Command("report"))
@router.message(lambda message: message.text in ["📝 Отправить отчет", "Отправить отчет"])
async def cmd_report(message: Message, state: FSMContext):
    """Handle /report command."""
    await message.answer(
        "🎤 <b>Отправь голосовое сообщение с отчетом</b>\n\n"
        "Не забудь указать:\n"
        "• Дату работы\n"
        "• Номер техники\n"
        "• Номер бригады\n"
        "• Описание работ"
    )
    await state.set_state(ReportStates.waiting_for_voice)


@router.message(Command("my_reports"))
@router.message(lambda message: message.text in ["📊 Мои отчеты", "Мои отчеты"])
async def cmd_my_reports(message: Message, user_id: str):
    """Handle /my_reports command."""
    await message.answer(
        "📊 <b>Выбери период для просмотра отчетов:</b>", reply_markup=get_period_keyboard()
    )


@router.callback_query(F.data.startswith("period_"))
async def handle_period_selection(callback: CallbackQuery, user_id: str):
    """Handle period selection for viewing reports."""
    period = callback.data.replace("period_", "")

    # Calculate date range
    today = datetime.now().date()
    if period == "today":
        start_date = today
        end_date = today
        period_text = "сегодня"
    elif period == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = start_date
        period_text = "вчера"
    elif period == "week":
        start_date = today - timedelta(days=7)
        end_date = today
        period_text = "за неделю"
    elif period == "month":
        start_date = today - timedelta(days=30)
        end_date = today
        period_text = "за месяц"
    else:
        await callback.answer("Эта функция пока в разработке")
        return

    # Fetch reports
    reports = await report_service.get_user_reports(user_id, start_date, end_date)

    if not reports:
        await callback.message.edit_text(
            f"📭 У вас нет отчетов {period_text}.", reply_markup=None
        )
        return

    # Format and send reports
    reports_text = f"📊 <b>Ваши отчеты {period_text}:</b>\n\n"
    for i, report in enumerate(reports, 1):
        reports_text += f"<b>{i}. {report.report_date}</b>\n"
        reports_text += f"🚜 Техника: {report.equipment_number}\n"
        reports_text += f"👷 Бригада: {report.brigade_number}\n"
        reports_text += f"📝 {report.work_description[:100]}...\n"
        reports_text += "\n"

    await callback.message.edit_text(reports_text, reply_markup=None)
    await callback.answer()


@router.message(Command("edit_last"))
@router.message(lambda message: message.text in ["✏️ Исправить отчет", "Исправить отчет"])
async def cmd_edit_last(message: Message, user_id: str):
    """Handle /edit_last command."""
    # Get last report
    last_report = await report_service.get_last_user_report(user_id)

    if not last_report:
        await message.answer("📭 У вас пока нет отчетов для редактирования.")
        return

    report_text = f"""
📝 <b>Ваш последний отчет:</b>

📅 Дата: {last_report.report_date}
🚜 Техника: {last_report.equipment_number}
👷 Бригада: {last_report.brigade_number}
📝 Работы: {last_report.work_description}

Что нужно исправить? Отправь голосовое или текстовое сообщение.
"""

    await message.answer(report_text)


@router.callback_query(F.data == "confirm_report")
async def handle_confirm_report(callback: CallbackQuery, state: FSMContext, user_id: str):
    """Handle report confirmation."""
    data = await state.get_data()
    report_data = data.get("report_data")

    if not report_data:
        await callback.answer("Ошибка: данные отчета не найдены")
        return

    try:
        # Save report to database
        await report_service.save_report(user_id, report_data)

        await callback.message.edit_text(
            "✅ <b>Отчет сохранен!</b>\n\n"
            "Спасибо за работу. Можешь отправить следующий отчет в любое время.",
            reply_markup=None,
        )

        # Clear state
        await state.clear()
        await callback.answer("Отчет сохранен!")

    except Exception as e:
        logger.error(f"Error saving report: {e}", exc_info=True)
        await callback.answer("Ошибка при сохранении отчета", show_alert=True)


@router.callback_query(F.data == "edit_report")
async def handle_edit_request(callback: CallbackQuery, state: FSMContext):
    """Handle request to edit report."""
    await callback.message.edit_text(
        "✏️ Что нужно исправить?\n\nОтправь голосовое или текстовое сообщение с изменениями.",
        reply_markup=None,
    )
    await state.set_state(ReportStates.waiting_for_correction)
    await callback.answer()


@router.callback_query(F.data == "cancel_report")
async def handle_cancel_report(callback: CallbackQuery, state: FSMContext):
    """Handle report cancellation."""
    await callback.message.edit_text(
        "❌ Отчет отменен.\n\nИспользуй /report для создания нового отчета.", reply_markup=None
    )
    await state.clear()
    await callback.answer("Отчет отменен")
