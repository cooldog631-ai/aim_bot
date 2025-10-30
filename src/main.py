"""Main entry point for the AI Voice Reports Bot."""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Main application entry point."""
    # Import here to avoid circular imports
    from src.bot.messenger_manager import MessengerManager
    from src.database.session import init_db

    # Initialize database
    try:
        logger.info("📊 Initializing database...")
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        sys.exit(1)

    # Start messenger(s)
    try:
        manager = MessengerManager()
        await manager.start()

    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down gracefully...")
        if 'manager' in locals():
            await manager.stop()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Goodbye!")
