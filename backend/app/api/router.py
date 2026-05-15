"""
Main API Router
Centralizes all API endpoints
"""

from fastapi import APIRouter
from app.api.endpoints import fir, analysis, health

router = APIRouter(prefix="/api/v1")

# Include endpoint routers
router.include_router(health.router, tags=["Health"])
router.include_router(fir.router, tags=["FIR Processing"], prefix="/fir")
router.include_router(analysis.router, tags=["Analysis"], prefix="/analysis")
