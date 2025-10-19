"""Yelp Business API tools"""

import logging
from typing import Dict, Any, Optional
import httpx

from app.config import settings
from app.core.cache import cached

logger = logging.getLogger(__name__)


async def search_businesses(
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    term: Optional[str] = None,
    categories: Optional[str] = None,
    price: Optional[str] = None,
    radius: int = 5000,
    limit: int = 20,
    sort_by: str = "best_match"
) -> Dict[str, Any]:
    """
    Search for businesses on Yelp
    
    Args:
        location: Location string (e.g., "San Francisco, CA")
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        term: Search term (e.g., "pizza", "italian")
        categories: Category filter (e.g., "restaurants,bars")
        price: Price filter (e.g., "1,2,3,4")
        radius: Search radius in meters (max 40000)
        limit: Number of results (max 50)
        sort_by: Sort order (best_match, rating, review_count, distance)
        
    Returns:
        Dictionary with businesses and total count
    """
    try:
        params = {
            "limit": min(limit, 50),
            "radius": min(radius, 40000),
            "sort_by": sort_by
        }
        
        # Location parameters
        if latitude and longitude:
            params["latitude"] = latitude
            params["longitude"] = longitude
        elif location:
            params["location"] = location
        else:
            raise ValueError("Either location or lat/lng must be provided")
        
        # Optional filters
        if term:
            params["term"] = term
        if categories:
            params["categories"] = categories
        if price:
            params["price"] = price
        
        headers = {
            "Authorization": f"Bearer {settings.yelp_api_key}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.yelp.com/v3/businesses/search",
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Found {data.get('total', 0)} businesses")
            return data
    
    except httpx.HTTPStatusError as e:
        logger.error(f"Yelp API error: {e.response.status_code} - {e.response.text}")
        return {"businesses": [], "total": 0}
    except Exception as e:
        logger.error(f"Error searching businesses: {e}")
        return {"businesses": [], "total": 0}


@cached(ttl=3600, key_prefix="yelp_business:")
async def get_business(business_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific business
    
    Args:
        business_id: Yelp business ID
        
    Returns:
        Business details dictionary
    """
    try:
        headers = {
            "Authorization": f"Bearer {settings.yelp_api_key}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.yelp.com/v3/businesses/{business_id}",
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPStatusError as e:
        logger.error(f"Yelp API error: {e.response.status_code}")
        return {}
    except Exception as e:
        logger.error(f"Error getting business {business_id}: {e}")
        return {}


async def autocomplete(text: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get autocomplete suggestions for business search
    
    Args:
        text: Search text
        latitude: User latitude
        longitude: User longitude
        
    Returns:
        Autocomplete suggestions
    """
    try:
        headers = {
            "Authorization": f"Bearer {settings.yelp_api_key}"
        }
        
        params = {
            "text": text,
            "latitude": latitude,
            "longitude": longitude
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.yelp.com/v3/autocomplete",
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    except Exception as e:
        logger.error(f"Error getting autocomplete suggestions: {e}")
        return {"terms": [], "businesses": [], "categories": []}

