# Setup Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Telegram Bot Token (from @BotFather)
- OpenAI API Key or Anthropic API Key (optional)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/cooldog631-ai/aim_bot.git
cd aim_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use any text editor
```

Required variables:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `OPENAI_API_KEY` - OpenAI API key (for Whisper and GPT)
- `ANTHROPIC_API_KEY` - Anthropic API key (optional, for Claude)

### 5. Initialize Database

```bash
# Initialize database
python scripts/init_db.py

# Or use Makefile
make init-db
```

### 6. Create Admin User (Optional)

```bash
python scripts/add_admin.py <your_telegram_id> "Your Name" --username your_username
```

To find your Telegram ID, message @userinfobot on Telegram.

### 7. Seed Test Data (Optional)

```bash
python scripts/seed_data.py
```

## Running the Bot

### Development Mode

```bash
python src/main.py

# Or use Makefile
make run
```

### Production Mode

```bash
# Set DEBUG=false in .env
DEBUG=false python src/main.py
```

## Running the API Server

```bash
uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port 8000
```

API documentation will be available at http://localhost:8000/docs

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Or use Makefile
make test
```

## Docker Deployment (Coming Soon)

```bash
# Build image
make docker-build

# Start services
make docker-up
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues, try:

```bash
# Delete existing database
rm aim_bot.db

# Reinitialize
python scripts/init_db.py
```

### Module Import Errors

Ensure you're running from the project root directory and virtual environment is activated.

### Bot Not Responding

1. Check that `TELEGRAM_BOT_TOKEN` is correct in `.env`
2. Verify bot is started: `/start` command in Telegram
3. Check logs in `logs/aim_bot.log`

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the codebase
- Check [API.md](./API.md) for API documentation
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
