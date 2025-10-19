"""Health check endpoints"""

import logging
from fastapi import APIRouter, status
from pydantic import BaseModel

from app.config import settings
from app.mcp_server.client import mcp_client
from app.core.cache import cache_manager
from app.core.vector_store import vector_store

logger = logging.getLogger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    environment: str
    services: dict


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Check application health and service status
    """
    services = {
        "mcp_server": "unknown",
        "cache": "unknown",
        "vector_db": "unknown"
    }
    
    # Check MCP server
    try:
        if mcp_client._connected:
            services["mcp_server"] = "healthy"
        else:
            services["mcp_server"] = "disconnected"
    except Exception as e:
        logger.error(f"MCP server health check failed: {e}")
        services["mcp_server"] = "unhealthy"
    
    # Check cache
    try:
        if cache_manager._connected:
            services["cache"] = "healthy"
        else:
            services["cache"] = "disconnected"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        services["cache"] = "unhealthy"
    
    # Check vector DB
    try:
        if vector_store._initialized:
            stats = await vector_store.get_collection_stats()
            if stats:
                services["vector_db"] = "healthy"
            else:
                services["vector_db"] = "unhealthy"
        else:
            services["vector_db"] = "not_initialized"
    except Exception as e:
        logger.error(f"Vector DB health check failed: {e}")
        services["vector_db"] = "unhealthy"
    
    return HealthResponse(
        status="healthy" if all(s == "healthy" for s in services.values()) else "degraded",
        version="1.0.0",
        environment=settings.app_env,
        services=services
    )


@router.get("/readiness")
async def readiness_check():
    """
    Check if application is ready to serve requests
    """
    ready = (
        mcp_client._connected and
        cache_manager._connected
    )
    
    if ready:
        return {"status": "ready"}
    else:
        return {"status": "not_ready"}, 503


@router.get("/liveness")
async def liveness_check():
    """
    Check if application is alive
    """
    return {"status": "alive"}

