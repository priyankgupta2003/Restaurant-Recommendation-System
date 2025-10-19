"""Yelp Reviews API tools"""

import logging
from typing import Dict, Any
import httpx

from app.config import settings
from app.core.cache import cached

logger = logging.getLogger(__name__)


@cached(ttl=3600, key_prefix="yelp_reviews:")
async def get_reviews(business_id: str, limit: int = 3) -> Dict[str, Any]:
    """
    Get reviews for a specific business
    
    Args:
        business_id: Yelp business ID
        limit: Number of reviews to retrieve (max 3)
        
    Returns:
        Dictionary with reviews and review count
    """
    try:
        headers = {
            "Authorization": f"Bearer {settings.yelp_api_key}"
        }
        
        params = {
            "limit": min(limit, 3)  # Yelp API max is 3
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.yelp.com/v3/businesses/{business_id}/reviews",
                params=params,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPStatusError as e:
        logger.error(f"Yelp API error: {e.response.status_code}")
        return {"reviews": [], "total": 0}
    except Exception as e:
        logger.error(f"Error getting reviews for {business_id}: {e}")
        return {"reviews": [], "total": 0}

