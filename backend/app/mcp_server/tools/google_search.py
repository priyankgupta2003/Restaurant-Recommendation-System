"""Google Places Search API tools"""

import logging
from typing import List, Dict, Any, Optional
import httpx

from app.config import settings
from app.core.cache import cached

logger = logging.getLogger(__name__)


@cached(ttl=3600, key_prefix="places_search:")
async def search_places(
    query: str,
    location: Optional[Dict[str, float]] = None,
    radius: int = 5000
) -> List[Dict[str, Any]]:
    """
    Search for places using Google Places API
    
    Args:
        query: Search query
        location: Optional dict with latitude and longitude
        radius: Search radius in meters
        
    Returns:
        List of place results
    """
    try:
        params = {
            "query": query,
            "key": settings.google_maps_api_key
        }
        
        if location:
            params["location"] = f"{location['latitude']},{location['longitude']}"
            params["radius"] = radius
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/textsearch/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("results", [])
            else:
                logger.warning(f"Places search failed: {data.get('status')}")
                return []
    
    except Exception as e:
        logger.error(f"Error searching places for query '{query}': {e}")
        return []


@cached(ttl=3600, key_prefix="nearby_search:")
async def search_nearby(
    latitude: float,
    longitude: float,
    radius: int = 5000,
    type_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Search for nearby places
    
    Args:
        latitude: Center point latitude
        longitude: Center point longitude
        radius: Search radius in meters
        type_filter: Optional place type filter (e.g., 'restaurant')
        
    Returns:
        List of nearby places
    """
    try:
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": settings.google_maps_api_key
        }
        
        if type_filter:
            params["type"] = type_filter
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/nearbysearch/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("results", [])
            else:
                logger.warning(f"Nearby search failed: {data.get('status')}")
                return []
    
    except Exception as e:
        logger.error(f"Error searching nearby places: {e}")
        return []


@cached(ttl=86400, key_prefix="place_details:")
async def get_place_details(place_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a place
    
    Args:
        place_id: Google Place ID
        
    Returns:
        Place details dictionary
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/details/json",
                params={
                    "place_id": place_id,
                    "key": settings.google_maps_api_key,
                    "fields": "name,rating,formatted_address,formatted_phone_number,opening_hours,website,price_level,photos"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("result", {})
            else:
                logger.warning(f"Place details failed: {data.get('status')}")
                return {}
    
    except Exception as e:
        logger.error(f"Error getting place details for {place_id}: {e}")
        return {}

