# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers.score_router import router as score_router

settings = get_settings()

# ---------------------------------------------------------
# FastAPI Application Configuration
# ---------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)


# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------
# Allow all origins in development, restricted in production
allowed_origins = ["*"] if settings.environment != "production" else settings.allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(score_router)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/", tags=["health"])
def health_check():
    """
    Basic health endpoint for uptime monitoring and CI/CD readiness.
    """
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
