"""Chat data models"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class ChatSession(BaseModel):
    """Chat session model"""
    session_id: str = Field(..., description="Unique session identifier")
    messages: List[Message] = Field(default_factory=list, description="Conversation history")
    user_preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences")
    location: Optional[Dict[str, Any]] = Field(default=None, description="User location")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationContext(BaseModel):
    """Conversation context for RAG"""
    query: str = Field(..., description="User query")
    chat_history: List[Message] = Field(default_factory=list, description="Previous messages")
    location: Optional[Dict[str, Any]] = Field(default=None, description="User location")
    preferences: Optional[Dict[str, Any]] = Field(default=None, description="User preferences")
    retrieved_context: Optional[List[Dict[str, Any]]] = Field(default=None, description="Retrieved documents")

