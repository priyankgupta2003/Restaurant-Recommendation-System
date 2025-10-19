"""MCP Client for FastAPI application"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class MCPClient:
    """
    Client to interact with the unified MCP server
    
    This client provides a simplified interface to call MCP tools
    from the FastAPI application.
    """
    
    def __init__(self):
        self._connected = False
        # Tool implementations will be imported here
        from app.mcp_server.tools import (
            google_location,
            google_search,
            yelp_business,
            yelp_reviews,
            vectordb
        )
        self.google_location = google_location
        self.google_search = google_search
        self.yelp_business = yelp_business
        self.yelp_reviews = yelp_reviews
        self.vectordb = vectordb
    
    async def connect(self):
        """Initialize MCP client"""
        if not self._connected:
            logger.info("Initializing MCP client...")
            # Initialize any necessary connections
            self._connected = True
            logger.info("MCP client initialized successfully")
    
    async def close(self):
        """Close MCP client"""
        if self._connected:
            logger.info("Closing MCP client...")
            self._connected = False
            logger.info("MCP client closed")
    
    # ===== Google Location Tools =====
    
    async def geocode(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates"""
        return await self.google_location.geocode(address)
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Convert coordinates to address"""
        return await self.google_location.reverse_geocode(latitude, longitude)
    
    async def calculate_distance(
        self,
        origin_lat: float,
        origin_lng: float,
        dest_lat: float,
        dest_lng: float
    ) -> float:
        """Calculate distance between two points"""
        return await self.google_location.calculate_distance(
            origin_lat, origin_lng, dest_lat, dest_lng
        )
    
    # ===== Google Search Tools =====
    
    async def search_places(
        self,
        query: str,
        location: Optional[Dict[str, float]] = None,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Search for places"""
        return await self.google_search.search_places(query, location, radius)
    
    async def search_nearby(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000,
        type_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search nearby places"""
        return await self.google_search.search_nearby(
            latitude, longitude, radius, type_filter
        )
    
    # ===== Yelp Business Tools =====
    
    async def search_restaurants(
        self,
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
        """Search restaurants on Yelp"""
        return await self.yelp_business.search_businesses(
            location=location,
            latitude=latitude,
            longitude=longitude,
            term=term,
            categories=categories,
            price=price,
            radius=radius,
            limit=limit,
            sort_by=sort_by
        )
    
    async def get_business_details(self, business_id: str) -> Dict[str, Any]:
        """Get detailed business information"""
        return await self.yelp_business.get_business(business_id)
    
    # ===== Yelp Reviews Tools =====
    
    async def get_business_reviews(
        self,
        business_id: str,
        limit: int = 3
    ) -> Dict[str, Any]:
        """Get business reviews"""
        return await self.yelp_reviews.get_reviews(business_id, limit)
    
    # ===== Vector DB Tools =====
    
    async def store_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]]
    ) -> bool:
        """Store embeddings in vector database"""
        return await self.vectordb.store_embeddings(ids, embeddings, metadata)
    
    async def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        return await self.vectordb.search_similar(query_embedding, top_k, filters)
    
    async def search_hybrid(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """Hybrid search: generate embedding and search"""
        return await self.vectordb.search_hybrid(query, filters, top_k)
    
    async def update_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]]
    ) -> bool:
        """Update existing embeddings"""
        return await self.vectordb.update_embeddings(ids, embeddings, metadata)
    
    async def delete_embeddings(self, ids: List[str]) -> bool:
        """Delete embeddings"""
        return await self.vectordb.delete_embeddings(ids)
    
    async def get_vector_stats(self) -> Dict[str, Any]:
        """Get vector database statistics"""
        return await self.vectordb.get_stats()


# Global MCP client instance
mcp_client = MCPClient()

