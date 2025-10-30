"""FastAPI application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import analytics, employees, reports
from src.config import get_settings
from src.database.session import close_db, init_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting API server...")
    await init_db()
    logger.info("API server started")

    yield

    # Shutdown
    logger.info("Shutting down API server...")
    await close_db()
    logger.info("API server stopped")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="AI Voice Reports Bot API",
        description="REST API for voice reports management and analytics",
        version="0.1.0",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
    app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
    app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "AI Voice Reports Bot API",
            "version": "0.1.0",
            "docs": "/docs",
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app
