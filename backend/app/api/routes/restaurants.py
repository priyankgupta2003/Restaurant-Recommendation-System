"""Restaurant API endpoints"""

import logging
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional

from app.schemas.restaurant_schemas import (
    RestaurantSearchRequest,
    RestaurantSearchResponse,
    RestaurantDetailsRequest
)
from app.mcp_server.client import mcp_client
from app.models.restaurant import Restaurant

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/restaurants/search", response_model=RestaurantSearchResponse)
async def search_restaurants(request: RestaurantSearchRequest):
    """
    Search for restaurants
    
    Args:
        request: Search parameters
        
    Returns:
        List of matching restaurants
    """
    try:
        # Search using Yelp
        result = await mcp_client.search_restaurants(
            location=request.location,
            latitude=request.latitude,
            longitude=request.longitude,
            term=request.query,
            categories=request.categories,
            price=request.price,
            radius=request.radius,
            limit=request.limit,
            sort_by=request.sort_by
        )
        
        businesses = result.get("businesses", [])
        total = result.get("total", 0)
        
        return RestaurantSearchResponse(
            restaurants=businesses,
            total=total,
            query=request.query
        )
    
    except Exception as e:
        logger.error(f"Error searching restaurants: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search restaurants"
        )


@router.get("/restaurants/{restaurant_id}")
async def get_restaurant_details(
    restaurant_id: str,
    include_reviews: bool = Query(default=True)
):
    """
    Get detailed information about a restaurant
    
    Args:
        restaurant_id: Restaurant ID
        include_reviews: Whether to include reviews
        
    Returns:
        Restaurant details
    """
    try:
        # Get business details
        business = await mcp_client.get_business_details(restaurant_id)
        
        if not business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        
        # Get reviews if requested
        if include_reviews:
            reviews_data = await mcp_client.get_business_reviews(restaurant_id, limit=3)
            business["reviews"] = reviews_data.get("reviews", [])
        
        return business
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting restaurant details: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get restaurant details"
        )


@router.get("/restaurants/nearby")
async def get_nearby_restaurants(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius: int = Query(default=5000, description="Search radius in meters"),
    limit: int = Query(default=20, ge=1, le=50)
):
    """
    Get restaurants near a location
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in meters
        limit: Number of results
        
    Returns:
        List of nearby restaurants
    """
    try:
        result = await mcp_client.search_restaurants(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            limit=limit,
            categories="restaurants"
        )
        
        return {
            "restaurants": result.get("businesses", []),
            "total": result.get("total", 0)
        }
    
    except Exception as e:
        logger.error(f"Error getting nearby restaurants: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get nearby restaurants"
        )

