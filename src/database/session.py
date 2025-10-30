"""Database session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import get_settings
from src.database.base import Base
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Global engine and session maker
engine = None
async_session_maker = None


def get_async_db_url(sync_url: str) -> str:
    """Convert sync database URL to async URL."""
    if sync_url.startswith("sqlite:///"):
        return sync_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    elif sync_url.startswith("postgresql://"):
        return sync_url.replace("postgresql://", "postgresql+asyncpg://")
    return sync_url


async def init_db():
    """Initialize database engine and create tables."""
    global engine, async_session_maker

    settings = get_settings()
    db_url = get_async_db_url(settings.database_url)

    logger.info(f"Initializing database: {db_url.split('@')[-1] if '@' in db_url else db_url}")

    # Create async engine
    engine = create_async_engine(
        db_url,
        echo=settings.debug,
        future=True,
    )

    # Create session maker
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized successfully")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.

    Usage:
        async with get_db() as db:
            # use db
    """
    if async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def close_db():
    """Close database connections."""
    global engine
    if engine:
        await engine.dispose()
        logger.info("Database connections closed")
