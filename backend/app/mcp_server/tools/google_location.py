"""Google Location API tools"""

import logging
from typing import Dict, Any
import httpx
from math import radians, cos, sin, asin, sqrt

from app.config import settings
from app.core.cache import cached

logger = logging.getLogger(__name__)


@cached(ttl=86400, key_prefix="geo:")
async def geocode(address: str) -> Dict[str, Any]:
    """
    Convert address to latitude/longitude coordinates
    
    Args:
        address: Address string to geocode
        
    Returns:
        Dictionary with lat, lng, and formatted address
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={
                    "address": address,
                    "key": settings.google_maps_api_key
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                location = result["geometry"]["location"]
                
                return {
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "formatted_address": result["formatted_address"],
                    "place_id": result.get("place_id")
                }
            else:
                logger.warning(f"Geocoding failed for address: {address}")
                return {}
    
    except Exception as e:
        logger.error(f"Error geocoding address {address}: {e}")
        return {}


@cached(ttl=86400, key_prefix="reverse_geo:")
async def reverse_geocode(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Convert latitude/longitude to address
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Dictionary with address information
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/geocode/json",
                params={
                    "latlng": f"{latitude},{longitude}",
                    "key": settings.google_maps_api_key
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                
                # Extract address components
                address_components = {}
                for component in result.get("address_components", []):
                    types = component.get("types", [])
                    if "locality" in types:
                        address_components["city"] = component["long_name"]
                    elif "administrative_area_level_1" in types:
                        address_components["state"] = component["short_name"]
                    elif "postal_code" in types:
                        address_components["zip_code"] = component["long_name"]
                    elif "country" in types:
                        address_components["country"] = component["short_name"]
                
                return {
                    "formatted_address": result["formatted_address"],
                    "place_id": result.get("place_id"),
                    **address_components
                }
            else:
                logger.warning(f"Reverse geocoding failed for {latitude}, {longitude}")
                return {}
    
    except Exception as e:
        logger.error(f"Error reverse geocoding {latitude}, {longitude}: {e}")
        return {}


async def calculate_distance(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float
) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    
    Args:
        origin_lat: Origin latitude
        origin_lng: Origin longitude
        dest_lat: Destination latitude
        dest_lng: Destination longitude
        
    Returns:
        Distance in meters
    """
    # Convert to radians
    origin_lat, origin_lng, dest_lat, dest_lng = map(
        radians, [origin_lat, origin_lng, dest_lat, dest_lng]
    )
    
    # Haversine formula
    dlng = dest_lng - origin_lng
    dlat = dest_lat - origin_lat
    a = sin(dlat / 2) ** 2 + cos(origin_lat) * cos(dest_lat) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in meters
    r = 6371000
    
    return c * r

