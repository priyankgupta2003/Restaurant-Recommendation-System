"""Chat API schemas"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.models.restaurant import Restaurant


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., description="User message", min_length=1)
    session_id: Optional[str] = Field(default=None, description="Chat session ID")
    location: Optional[Dict[str, Any]] = Field(default=None, description="User location")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences")


class ChatResponse(BaseModel):
    """Chat response schema"""
    message: str = Field(..., description="Assistant response")
    session_id: str = Field(..., description="Chat session ID")
    restaurants: Optional[List[Restaurant]] = Field(default=None, description="Recommended restaurants")
    suggestions: Optional[List[str]] = Field(default=None, description="Follow-up suggestions")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class StreamingChatChunk(BaseModel):
    """Streaming chat chunk schema"""
    type: str = Field(..., description="Chunk type: text, restaurant, or end")
    content: Optional[str] = Field(default=None, description="Text content")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Structured data")

