"""RAG (Retrieval-Augmented Generation) service"""

import logging
import re
from typing import List, Dict, Any, Optional

from app.mcp_server.client import mcp_client
from app.models.chat import ConversationContext

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG pipeline operations"""
    
    def __init__(self):
        self.cuisine_keywords = [
            "italian", "chinese", "japanese", "mexican", "thai", "indian",
            "french", "korean", "vietnamese", "mediterranean", "american",
            "pizza", "sushi", "burgers", "tacos", "pasta", "seafood"
        ]
        self.price_keywords = {
            "cheap": "1",
            "affordable": "1,2",
            "moderate": "2",
            "expensive": "3,4",
            "fine dining": "4"
        }
    
    async def retrieve_restaurants(
        self,
        context: ConversationContext
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant restaurants using hybrid approach
        
        Args:
            context: Conversation context with query and preferences
            
        Returns:
            List of relevant restaurants
        """
        query = context.query
        location = context.location
        preferences = context.preferences or {}
        
        # Extract search parameters from query
        search_params = self._extract_search_params(query, preferences)
        
        # Get location coordinates if address is provided
        location_data = None
        if location and "address" in location:
            location_data = await mcp_client.geocode(location["address"])
        elif location and "latitude" in location:
            location_data = location
        
        # Search using Yelp API
        yelp_results = await self._search_yelp(search_params, location_data)
        
        # Search using vector DB for semantic similarity
        vector_results = await self._search_vector_db(query, location_data)
        
        # Merge and deduplicate results
        merged_results = self._merge_results(yelp_results, vector_results)
        
        # Enrich with reviews
        enriched_results = await self._enrich_with_reviews(merged_results[:10])
        
        return enriched_results
    
    def _extract_search_params(
        self,
        query: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract search parameters from query and preferences"""
        query_lower = query.lower()
        params = {}
        
        # Extract cuisine type
        for cuisine in self.cuisine_keywords:
            if cuisine in query_lower:
                params["term"] = cuisine
                params["categories"] = "restaurants"
                break
        
        # Extract price range
        for price_term, price_value in self.price_keywords.items():
            if price_term in query_lower:
                params["price"] = price_value
                break
        
        # Extract rating requirement
        rating_match = re.search(r'(\d\.?\d*)\s*star', query_lower)
        if rating_match:
            params["min_rating"] = float(rating_match.group(1))
        
        # Apply preferences
        if "cuisine" in preferences:
            params["term"] = preferences["cuisine"]
        if "price_range" in preferences:
            params["price"] = preferences["price_range"]
        if "dietary" in preferences:
            # Add dietary restrictions to search term
            dietary = preferences["dietary"]
            if "term" in params:
                params["term"] += f" {dietary}"
            else:
                params["term"] = dietary
        
        return params
    
    async def _search_yelp(
        self,
        search_params: Dict[str, Any],
        location_data: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search restaurants using Yelp API"""
        try:
            kwargs = {
                "limit": 20,
                "sort_by": "best_match",
                **search_params
            }
            
            if location_data:
                if "latitude" in location_data:
                    kwargs["latitude"] = location_data["latitude"]
                    kwargs["longitude"] = location_data["longitude"]
                elif "address" in location_data:
                    kwargs["location"] = location_data["address"]
            
            result = await mcp_client.search_restaurants(**kwargs)
            
            businesses = result.get("businesses", [])
            
            # Filter by rating if specified
            min_rating = search_params.get("min_rating")
            if min_rating:
                businesses = [b for b in businesses if b.get("rating", 0) >= min_rating]
            
            return businesses
        
        except Exception as e:
            logger.error(f"Error searching Yelp: {e}")
            return []
    
    async def _search_vector_db(
        self,
        query: str,
        location_data: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Search restaurants using vector database"""
        try:
            filters = {}
            
            if location_data and "latitude" in location_data:
                # Could add location-based filtering if vector DB supports it
                pass
            
            results = await mcp_client.search_hybrid(
                query=query,
                filters=filters,
                top_k=20
            )
            
            return [r["metadata"] for r in results if "metadata" in r]
        
        except Exception as e:
            logger.error(f"Error searching vector DB: {e}")
            return []
    
    def _merge_results(
        self,
        yelp_results: List[Dict[str, Any]],
        vector_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Merge and deduplicate results from different sources"""
        # Use dict to deduplicate by business ID
        merged = {}
        
        # Add Yelp results (prioritize these)
        for business in yelp_results:
            business_id = business.get("id")
            if business_id:
                merged[business_id] = business
        
        # Add vector DB results if not already present
        for business in vector_results:
            business_id = business.get("id") or business.get("yelp_id")
            if business_id and business_id not in merged:
                merged[business_id] = business
        
        # Convert back to list and sort by rating
        results = list(merged.values())
        results.sort(key=lambda x: (x.get("rating", 0), x.get("review_count", 0)), reverse=True)
        
        return results
    
    async def _enrich_with_reviews(
        self,
        restaurants: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Enrich restaurant data with reviews"""
        enriched = []
        
        for restaurant in restaurants:
            business_id = restaurant.get("id")
            if business_id:
                try:
                    reviews_data = await mcp_client.get_business_reviews(business_id, limit=3)
                    restaurant["reviews"] = reviews_data.get("reviews", [])
                except Exception as e:
                    logger.warning(f"Failed to get reviews for {business_id}: {e}")
                    restaurant["reviews"] = []
            
            enriched.append(restaurant)
        
        return enriched


# Global RAG service instance
rag_service = RAGService()

