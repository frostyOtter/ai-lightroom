from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=dict[str, str])
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "service": "ai-lightroom-api"}


@router.get("/detailed", response_model=dict[str, Any])
async def detailed_health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "ai-lightroom-api",
        "components": {"database": "not configured", "gemini_api": "not configured"},
    }
