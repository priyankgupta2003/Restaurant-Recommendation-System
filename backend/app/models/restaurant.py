"""Restaurant data models"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location model"""
    latitude: float
    longitude: float
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class Category(BaseModel):
    """Restaurant category"""
    alias: str
    title: str


class Review(BaseModel):
    """Restaurant review"""
    id: str
    rating: float
    text: str
    time_created: str
    user_name: Optional[str] = None


class Restaurant(BaseModel):
    """Restaurant model"""
    id: str
    name: str
    rating: Optional[float] = None
    review_count: Optional[int] = 0
    price: Optional[str] = None
    categories: List[Category] = Field(default_factory=list)
    location: Optional[Location] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    url: Optional[str] = None
    is_closed: bool = False
    distance: Optional[float] = None
    reviews: Optional[List[Review]] = Field(default_factory=list)
    menu_summary: Optional[str] = None


class RestaurantSearchParams(BaseModel):
    """Search parameters for restaurants"""
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    term: Optional[str] = None
    categories: Optional[str] = None
    price: Optional[str] = None  # "1,2,3,4"
    radius: int = 5000  # meters
    limit: int = 20
    sort_by: Optional[str] = "best_match"  # best_match, rating, review_count, distance
    open_now: bool = False

