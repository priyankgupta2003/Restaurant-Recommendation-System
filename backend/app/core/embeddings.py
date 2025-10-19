"""Embedding generation utilities"""

import logging
from typing import List, Union
from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embeddings
        """
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    @staticmethod
    def prepare_restaurant_text(restaurant: dict) -> str:
        """
        Prepare restaurant data for embedding
        
        Args:
            restaurant: Restaurant data dictionary
            
        Returns:
            Formatted text for embedding
        """
        parts = [
            f"Name: {restaurant.get('name', '')}",
            f"Categories: {', '.join(restaurant.get('categories', []))}",
            f"Price Range: {restaurant.get('price', '')}",
            f"Rating: {restaurant.get('rating', '')}",
            f"Location: {restaurant.get('location', {}).get('address1', '')}",
            f"Description: {restaurant.get('description', '')}"
        ]
        return " | ".join(filter(None, parts))
    
    @staticmethod
    def prepare_review_text(review: dict) -> str:
        """
        Prepare review data for embedding
        
        Args:
            review: Review data dictionary
            
        Returns:
            Formatted text for embedding
        """
        parts = [
            f"Rating: {review.get('rating', '')}",
            f"Review: {review.get('text', '')}"
        ]
        return " | ".join(filter(None, parts))


# Global embedding service instance
embedding_service = EmbeddingService()

