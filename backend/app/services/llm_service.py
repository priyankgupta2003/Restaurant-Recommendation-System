"""LLM service for chat and text generation"""

import logging
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from app.config import settings
from app.models.chat import Message

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with Large Language Models"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        
        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        elif self.provider == "anthropic":
            self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
        
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
        self.max_tokens = settings.llm_max_tokens
    
    async def generate_response(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            Generated response text
        """
        try:
            if self.provider == "openai":
                return await self._generate_openai(
                    messages, system_prompt, temperature, max_tokens
                )
            elif self.provider == "anthropic":
                return await self._generate_anthropic(
                    messages, system_prompt, temperature, max_tokens
                )
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise
    
    async def _generate_openai(
        self,
        messages: List[Message],
        system_prompt: Optional[str],
        temperature: Optional[float],
        max_tokens: Optional[int]
    ) -> str:
        """Generate response using OpenAI API"""
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self,
        messages: List[Message],
        system_prompt: Optional[str],
        temperature: Optional[float],
        max_tokens: Optional[int]
    ) -> str:
        """Generate response using Anthropic API"""
        formatted_messages = []
        
        for msg in messages:
            if msg.role != "system":
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        response = await self.client.messages.create(
            model=self.model,
            system=system_prompt or "",
            messages=formatted_messages,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens
        )
        
        return response.content[0].text
    
    def build_restaurant_context(
        self,
        restaurants: List[Dict[str, Any]],
        query: str
    ) -> str:
        """
        Build context string from restaurant data
        
        Args:
            restaurants: List of restaurant dictionaries
            query: User query
            
        Returns:
            Formatted context string
        """
        context_parts = [
            f"User Query: {query}",
            "\nTop Restaurant Recommendations:\n"
        ]
        
        for idx, restaurant in enumerate(restaurants[:10], 1):
            name = restaurant.get("name", "Unknown")
            rating = restaurant.get("rating", "N/A")
            price = restaurant.get("price", "N/A")
            categories = ", ".join([cat.get("title", "") for cat in restaurant.get("categories", [])])
            location = restaurant.get("location", {})
            address = location.get("address1", "")
            city = location.get("city", "")
            review_count = restaurant.get("review_count", 0)
            
            context_parts.append(
                f"{idx}. {name}\n"
                f"   Rating: {rating} ({review_count} reviews)\n"
                f"   Price: {price}\n"
                f"   Cuisine: {categories}\n"
                f"   Location: {address}, {city}\n"
            )
            
            # Add reviews if available
            if "reviews" in restaurant and restaurant["reviews"]:
                context_parts.append("   Recent Reviews:\n")
                for review in restaurant["reviews"][:2]:
                    text = review.get("text", "")[:150]
                    context_parts.append(f"   - {text}...\n")
            
            context_parts.append("\n")
        
        return "".join(context_parts)


# Global LLM service instance
llm_service = LLMService()

