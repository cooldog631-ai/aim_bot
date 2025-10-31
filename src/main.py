"""
MVP: Простой Telegram бот для сбора голосовых отчётов
Запускается на Railway без БД и AI - только базовый функционал
"""

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не найден! Добавьте его в Railway Variables")

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я бот для сбора голосовых отчётов.\n\n"
        "📝 Отправь мне текстовое или голосовое сообщение, и я его обработаю!\n\n"
        "Доступные команды:\n"
        "/start - показать это сообщение\n"
        "/help - помощь"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(
        "ℹ️ Это MVP-версия бота для сбора отчётов.\n\n"
        "Сейчас бот просто принимает сообщения.\n"
        "В будущем добавим:\n"
        "- Распознавание голоса (Whisper)\n"
        "- Валидацию через AI\n"
        "- Сохранение в базу данных"
    )


@dp.message()
async def handle_message(message: types.Message):
    """Обработчик всех остальных сообщений"""
    if message.voice:
        await message.answer(
            "🎤 Получил голосовое сообщение!\n"
            f"Длительность: {message.voice.duration} сек\n\n"
            "⚠️ Распознавание голоса пока не подключено (требует настройки FFmpeg)"
        )
    elif message.text:
        await message.answer(
            f"✅ Получил текстовое сообщение:\n\n\"{message.text}\"\n\n"
            "В будущем здесь будет валидация через AI"
        )
    else:
        await message.answer("⚠️ Пока я умею работать только с текстом и голосом")


async def main():
    """Запуск бота"""
    logger.info("🚀 Запускаем бота...")
    logger.info(f"✅ Токен найден: {BOT_TOKEN[:10]}...")

    try:
        # Удаляем старые updates и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен")
