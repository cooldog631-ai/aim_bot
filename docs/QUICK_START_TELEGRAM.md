# Быстрый старт с Telegram Bot

## 📱 Шаг 1: Создать Telegram бота

1. Откройте Telegram и найдите **@BotFather**
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "AI Reports Bot")
   - Введите username (должен заканчиваться на "bot", например: "ai_reports_bot")
4. Сохраните полученный **Bot Token** (выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## ⚙️ Шаг 2: Настроить окружение

### Создать .env файл

```bash
cp .env.example .env
```

### Добавить токен в .env

Откройте `.env` и укажите ваш токен:

```bash
# Bot Configuration
MESSENGER_TYPE=telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# AI Services (для обработки голосовых)
OPENAI_API_KEY=your_openai_api_key_here

# Database (SQLite по умолчанию)
DATABASE_URL=sqlite:///./aim_bot.db

# Другие настройки оставить по умолчанию
```

## 📦 Шаг 3: Установить зависимости

```bash
# Создать виртуальное окружение (если еще не создано)
python -m venv venv

# Активировать
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

## 🗄️ Шаг 4: Инициализировать базу данных

```bash
python scripts/init_db.py
```

Вы должны увидеть:
```
✅ Database initialized successfully!
```

## 🚀 Шаг 5: Запустить бота

```bash
python src/main.py
```

Вы должны увидеть:
```
============================================================
🚀 Starting AI Voice Reports Bot...
============================================================
Messenger type: telegram
...
Initializing Telegram bot...
✅ Telegram bot initialized
✅ Handlers registered for telegram
🚀 Starting all messengers...
Starting Telegram bot...
✅ Telegram bot started!
Listening for messages...
```

## ✅ Шаг 6: Протестировать бота

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте `/start`

Бот должен ответить приветственным сообщением!

## 🎤 Тестирование голосовых отчетов

### Без AI (для теста структуры):

1. Отправьте голосовое сообщение
2. Бот скажет, что получил его
3. Без OPENAI_API_KEY транскрибация работать не будет

### С AI (полный функционал):

1. Получите OpenAI API ключ на https://platform.openai.com/api-keys
2. Добавьте в `.env`:
   ```bash
   OPENAI_API_KEY=sk-...
   ```
3. Перезапустите бота
4. Отправьте голосовое сообщение с отчетом:
   - "Сегодня 30 октября, работал на комбайне номер 15, бригада 3"
   - "Проводил техническое обслуживание и инструктаж"

Бот должен:
- Транскрибировать голос
- Извлечь данные
- Проверить полноту
- Попросить недостающую информацию (если нужно)

## 🔧 Полезные команды

```bash
# Остановить бота
Ctrl+C

# Посмотреть логи
tail -f logs/aim_bot.log

# Очистить базу данных
rm aim_bot.db
python scripts/init_db.py

# Добавить тестовые данные
python scripts/seed_data.py

# Запустить тесты
pytest
```

## 🐛 Troubleshooting

### Ошибка: "TELEGRAM_BOT_TOKEN not set"

Проверьте:
1. Файл `.env` существует
2. В нем есть строка `TELEGRAM_BOT_TOKEN=...`
3. Нет пробелов вокруг `=`

### Ошибка: "No module named 'aiogram'"

```bash
pip install -r requirements.txt
```

### Бот не отвечает

1. Проверьте, что бот запущен и видите "Listening for messages..."
2. Убедитесь, что отправляете команду правильному боту
3. Проверьте логи: `tail -f logs/aim_bot.log`

### Голосовые сообщения не обрабатываются

1. Убедитесь, что `OPENAI_API_KEY` установлен
2. Проверьте баланс на OpenAI аккаунте
3. Посмотрите логи на ошибки

## 📊 Просмотр данных

### Через SQLite CLI

```bash
sqlite3 aim_bot.db
sqlite> SELECT * FROM employees;
sqlite> SELECT * FROM reports;
sqlite> .quit
```

### Через API

Запустите API сервер:

```bash
uvicorn src.api.app:create_app --factory --reload
```

Откройте в браузере: http://localhost:8000/docs

## 🎯 Следующие шаги

1. ✅ Бот работает с командами
2. ✅ Тестируем голосовые сообщения
3. ⏭️ Настраиваем AI валидацию
4. ⏭️ Тестируем полный цикл отчета
5. ⏭️ Настраиваем права доступа
6. ⏭️ Деплоим на сервер

## 📚 Дополнительно

- Полная документация: `docs/SETUP.md`
- Архитектура: `docs/ARCHITECTURE.md`
- API документация: `docs/API.md`
- VK Max (когда будет доступно): `docs/VK_MAX_INTEGRATION.md`

---

**Готово! Бот работает в Telegram!** 🎉

Нужна помощь? Пишите issue или смотрите логи в `logs/aim_bot.log`
