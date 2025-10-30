# VK Max Integration Guide

## Overview

VK Max (ранее MAX) - это российский мессенджер от VK, запущенный в 2025 году. Бот поддерживает работу как с Telegram, так и с VK Max одновременно.

## Установка

### 1. Установить зависимости

```bash
pip install maxapi
```

Или обновить все зависимости:

```bash
pip install -r requirements.txt
```

### 2. Получить Bot Token от VK Max

1. Зарегистрируйтесь на платформе VK Max для разработчиков
2. Создайте нового бота
3. Получите Bot API Token

### 3. Настроить переменные окружения

Добавьте в `.env`:

```bash
MESSENGER_TYPE=vkmax  # или "both" для работы с Telegram и VK Max одновременно
VK_MAX_TOKEN=your_vk_max_bot_token_here
```

## Конфигурация

### Опции MESSENGER_TYPE

- `telegram` - только Telegram (по умолчанию)
- `vkmax` - только VK Max
- `both` - оба мессенджера одновременно

### Пример .env

```bash
# Использовать только VK Max
MESSENGER_TYPE=vkmax
VK_MAX_TOKEN=your_token_here

# Использовать оба мессенджера
MESSENGER_TYPE=both
TELEGRAM_BOT_TOKEN=your_telegram_token
VK_MAX_TOKEN=your_vkmax_token
```

## Поддерживаемые функции

### ✅ Реализовано

- Получение текстовых сообщений
- Получение голосовых сообщений
- Отправка текстовых сообщений
- Обработка команд (/start, /help)
- Unified интерфейс для обоих мессенджеров

### 🚧 В разработке

- Загрузка файлов (audio, voice)
- Скачивание файлов
- Inline кнопки (VK Max поддерживает)
- Webhook режим

### ❌ Не поддерживается VK Max

- HTML форматирование (как в Telegram)
- Некоторые специфичные для Telegram функции

## Типы сообщений

VK Max поддерживает:

- **Текстовые сообщения** (до 4,000 символов)
- **Голосовые сообщения** (audio attachment с transcription)
- **Фото**
- **Видео**
- **Файлы**
- **Стикеры**
- **Локация**
- **Контакты**

## Загрузка файлов (3-шаговый процесс)

```python
# 1. Получить upload URL
response = await bot.get_upload_url(file_type="audio")

# 2. Загрузить файл
# Upload binary data to URL

# 3. Прикрепить к сообщению
await bot.send_message(
    chat_id=chat_id,
    text="Голосовое сообщение",
    attachments=[{"type": "audio", "token": "file_token"}]
)
```

## Webhook vs Polling

### Polling (по умолчанию)

```python
await bot.start_polling(dispatcher)
```

- Простой в настройке
- Работает локально
- Не требует публичного URL

### Webhook

```python
await bot.set_webhook(url="https://yourdomain.com/webhook")
```

- Более эффективен для production
- Требует HTTPS
- Требует публичный URL

## Unified Handlers

Обработчики работают одинаково для обоих мессенджеров:

```python
async def handle_voice_message(context: MessageContext):
    """Работает и с Telegram, и с VK Max."""
    # Скачать голосовое сообщение
    voice_data = await context.download_voice()

    # Обработать
    # ...

    # Ответить
    await context.reply("Обработано!")
```

## Различия между Telegram и VK Max

| Функция | Telegram | VK Max |
|---------|----------|---------|
| HTML форматирование | ✅ | ❌ |
| Markdown | ✅ | ❌ |
| Inline кнопки | ✅ | ✅ |
| Voice messages | ✅ | ✅ |
| Файлы до 2GB | ✅ | ✅ |
| Стикеры | ✅ | ✅ |
| Боты в группах | ✅ | ✅ |

## Запуск

### Только VK Max

```bash
MESSENGER_TYPE=vkmax python src/main.py
```

### Оба мессенджера

```bash
MESSENGER_TYPE=both python src/main.py
```

## Troubleshooting

### ImportError: maxapi not found

```bash
pip install maxapi
# или
pip install git+https://github.com/max-messenger/max-botapi-python.git
```

### Bot не получает сообщения

1. Проверьте, что бот имеет права администратора в чате
2. Если настроен webhook, удалите его для polling:
   ```python
   await bot.delete_webhook()
   ```

### Голосовые сообщения не обрабатываются

VK Max отправляет голосовые сообщения как `audio` attachment с флагом transcription.
Убедитесь, что обработчик настроен на `content_types=["voice"]`.

## Примеры

### Базовый бот

```python
from src.bot.messenger_manager import MessengerManager

async def main():
    manager = MessengerManager()
    await manager.start()

asyncio.run(main())
```

### Отправка сообщения

```python
await bot.send_message(
    chat_id="chat_id",
    text="Привет!"
)
```

### Получение голосового сообщения

```python
@dp.message_created()
async def handle_voice(event: MessageCreated):
    if event.message.attachments:
        for att in event.message.attachments:
            if att.type == "audio":
                # Обработать audio
                token = att.payload.token
```

## Полезные ссылки

- [VK Max Bot API GitHub](https://github.com/max-messenger/max-botapi-python)
- [VK Max API Schema](https://github.com/max-messenger/max-bot-api-schema)
- [Официальная документация](https://dev.max.ru) (если доступна)

## Лицензия

VK Max Bot API распространяется под лицензией MIT.
