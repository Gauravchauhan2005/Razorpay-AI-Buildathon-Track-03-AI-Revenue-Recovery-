"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.database import create_tables
from app.core.config import settings
from app.core.logging_config import get_logger

# Import all models so they register with Base
import app.models  # noqa: F401

# Import routers
from app.api.webhook import router as webhook_router
from app.api.payments import router as payments_router
from app.api.recovery import router as recovery_router
from app.api.dashboard import router as dashboard_router

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager for FastAPI app."""
    logger.info("Starting Payment Recovery Agent...")
    create_tables()
    logger.info("Database tables created.")
    yield
    logger.info("Shutting down Payment Recovery Agent.")


app = FastAPI(
    title=settings.app_name,
    description="AI-powered autonomous payment recovery agent for Razorpay",
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(webhook_router)
app.include_router(payments_router, prefix="/api/v1")
app.include_router(recovery_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.app_name}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "docs": "/docs",
        "health": "/health",
    }
