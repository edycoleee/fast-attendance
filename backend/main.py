"""
RSUD Sulfat Attendance System API
FastAPI application with Clean Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.settings import settings
from config.database import Base, engine
from api.v1.router import api_router
from utils.middleware import RequestLoggingMiddleware
from utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from utils.logger import logger

# Create database tables (if using SQLAlchemy models)
# Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Log startup
logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "PostgreSQL",
        "docs": "/docs",
        "api_v1": settings.API_V1_PREFIX,
        "endpoints": {
            "lokasi": f"{settings.API_V1_PREFIX}/lokasi",
            "health": "/health"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "database": "PostgreSQL"
    }
