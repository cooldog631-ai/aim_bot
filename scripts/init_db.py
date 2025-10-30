"""Initialize database and create tables."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.session import init_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Initialize database."""
    logger.info("Initializing database...")

    try:
        await init_db()
        logger.info("✅ Database initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
