"""Chat service for orchestrating conversations"""

import logging
import uuid
from typing import List, Optional, Dict, Any

from app.models.chat import Message, ChatSession, ConversationContext
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service

logger = logging.getLogger(__name__)


class ChatService:
    """Service for managing chat conversations and generating responses"""
    
    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for the LLM"""
        return """You are a helpful restaurant recommendation assistant. Your role is to:
1. Help users find restaurants based on their preferences, location, and dietary needs
2. Provide detailed, personalized recommendations
3. Answer questions about restaurants, menus, reviews, and locations
4. Be conversational, friendly, and informative

When recommending restaurants:
- Consider the user's location, cuisine preferences, price range, and dietary restrictions
- Highlight key features like ratings, reviews, popular dishes, and ambiance
- Provide context from real reviews when available
- Suggest alternatives if the user's criteria are too restrictive
- Ask clarifying questions if the request is ambiguous

Format your responses in a natural, conversational way. When listing restaurants, be enthusiastic but honest about pros and cons."""
    
    async def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response
        
        Args:
            message: User message
            session_id: Optional session ID for conversation continuity
            location: Optional user location
            preferences: Optional user preferences
            
        Returns:
            Dictionary with response, session_id, and restaurants
        """
        try:
            # Get or create session
            if session_id and session_id in self.sessions:
                session = self.sessions[session_id]
            else:
                session_id = str(uuid.uuid4())
                session = ChatSession(
                    session_id=session_id,
                    user_preferences=preferences,
                    location=location
                )
                self.sessions[session_id] = session
            
            # Add user message to session
            user_message = Message(role="user", content=message)
            session.messages.append(user_message)
            
            # Build conversation context
            context = ConversationContext(
                query=message,
                chat_history=session.messages[:-1],  # Exclude current message
                location=location or session.location,
                preferences=preferences or session.user_preferences
            )
            
            # Retrieve relevant restaurants using RAG
            restaurants = await rag_service.retrieve_restaurants(context)
            context.retrieved_context = restaurants
            
            # Build context for LLM
            restaurant_context = llm_service.build_restaurant_context(restaurants, message)
            
            # Generate response
            messages_for_llm = [
                Message(role="user", content=restaurant_context + "\n\n" + message)
            ]
            
            # Add chat history (last 4 messages for context)
            if len(session.messages) > 1:
                messages_for_llm = session.messages[-4:-1] + messages_for_llm
            
            response_text = await llm_service.generate_response(
                messages=messages_for_llm,
                system_prompt=self.system_prompt
            )
            
            # Add assistant message to session
            assistant_message = Message(role="assistant", content=response_text)
            session.messages.append(assistant_message)
            
            # Generate follow-up suggestions
            suggestions = self._generate_suggestions(message, restaurants)
            
            return {
                "message": response_text,
                "session_id": session_id,
                "restaurants": restaurants[:10],  # Return top 10
                "suggestions": suggestions,
                "metadata": {
                    "total_restaurants_found": len(restaurants),
                    "location": context.location
                }
            }
        
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            raise
    
    def _generate_suggestions(
        self,
        query: str,
        restaurants: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate follow-up suggestions for the user"""
        suggestions = []
        
        query_lower = query.lower()
        
        # Suggest related cuisines
        if "italian" in query_lower and restaurants:
            suggestions.append("Show me Mediterranean restaurants nearby")
        elif "sushi" in query_lower or "japanese" in query_lower:
            suggestions.append("Any good Korean restaurants?")
        
        # Suggest price variations
        if "cheap" in query_lower or "affordable" in query_lower:
            suggestions.append("What about mid-range options?")
        elif "expensive" in query_lower or "fine dining" in query_lower:
            suggestions.append("Show me more affordable alternatives")
        
        # General suggestions
        if not suggestions:
            suggestions = [
                "Tell me more about the first restaurant",
                "Any vegetarian-friendly options?",
                "Show me restaurants with outdoor seating"
            ]
        
        return suggestions[:3]
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        return self.sessions.get(session_id)
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# Global chat service instance
chat_service = ChatService()

