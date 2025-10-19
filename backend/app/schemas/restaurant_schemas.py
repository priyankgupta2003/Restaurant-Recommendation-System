"""Restaurant API schemas"""

from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.restaurant import Restaurant


class RestaurantSearchRequest(BaseModel):
    """Restaurant search request schema"""
    query: Optional[str] = Field(default=None, description="Search query")
    location: Optional[str] = Field(default=None, description="Location string")
    latitude: Optional[float] = Field(default=None, description="Latitude")
    longitude: Optional[float] = Field(default=None, description="Longitude")
    categories: Optional[str] = Field(default=None, description="Category filters")
    price: Optional[str] = Field(default=None, description="Price range (1-4)")
    radius: int = Field(default=5000, description="Search radius in meters")
    limit: int = Field(default=20, description="Number of results")
    sort_by: str = Field(default="best_match", description="Sort order")


class RestaurantSearchResponse(BaseModel):
    """Restaurant search response schema"""
    restaurants: List[Restaurant] = Field(..., description="List of restaurants")
    total: int = Field(..., description="Total number of results")
    query: Optional[str] = Field(default=None, description="Original query")


class RestaurantDetailsRequest(BaseModel):
    """Restaurant details request schema"""
    restaurant_id: str = Field(..., description="Restaurant ID")
    include_reviews: bool = Field(default=True, description="Include reviews")

