"""Inline keyboards for bot interactions."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for report confirmation."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_report"),
                InlineKeyboardButton(text="✏️ Исправить", callback_data="edit_report"),
            ],
            [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_report")],
        ]
    )


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Отправить отчет"), KeyboardButton(text="📊 Мои отчеты")],
            [KeyboardButton(text="✏️ Исправить отчет"), KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )


def get_period_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for selecting report period."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Сегодня", callback_data="period_today"),
                InlineKeyboardButton(text="Вчера", callback_data="period_yesterday"),
            ],
            [
                InlineKeyboardButton(text="Неделя", callback_data="period_week"),
                InlineKeyboardButton(text="Месяц", callback_data="period_month"),
            ],
            [InlineKeyboardButton(text="Произвольный период", callback_data="period_custom")],
        ]
    )


def get_export_format_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for selecting export format."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📄 Excel", callback_data="export_xlsx"),
                InlineKeyboardButton(text="📝 CSV", callback_data="export_csv"),
            ],
            [InlineKeyboardButton(text="📋 PDF", callback_data="export_pdf")],
        ]
    )


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard with cancel button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")]]
    )
