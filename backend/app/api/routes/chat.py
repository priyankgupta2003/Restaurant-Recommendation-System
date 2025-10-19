"""Chat API endpoints"""

import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse

from app.schemas.chat_schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest):
    """
    Process a chat message and return recommendations
    
    Args:
        request: Chat request with message and optional session/location
        
    Returns:
        Chat response with AI message and restaurant recommendations
    """
    try:
        result = await chat_service.process_message(
            message=request.message,
            session_id=request.session_id,
            location=request.location,
            preferences=request.preferences
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request"
        )


@router.get("/chat/session/{session_id}")
async def get_session(session_id: str):
    """
    Get chat session history
    
    Args:
        session_id: Session ID
        
    Returns:
        Session data with message history
    """
    session = chat_service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return session


@router.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    """
    Clear a chat session
    
    Args:
        session_id: Session ID
        
    Returns:
        Success message
    """
    success = chat_service.clear_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return {"message": "Session cleared successfully"}

