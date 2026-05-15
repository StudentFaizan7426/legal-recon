"""
Health Check Endpoints
Endpoints for monitoring application health
"""

from fastapi import APIRouter, status
from app.config import get_settings
from app.models.schemas import HealthCheckResponse

router = APIRouter()
settings = get_settings()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running and healthy"
)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint
    Returns: HealthCheckResponse with application status
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT
    )


@router.get("/ready", status_code=status.HTTP_200_OK, summary="Readiness Check")
async def readiness_check():
    """
    Readiness check endpoint
    Returns: Status indicating if API is ready to handle requests
    """
    return {
        "status": "ready",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }
