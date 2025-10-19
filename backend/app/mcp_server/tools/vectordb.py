"""Vector Database tools"""

import logging
from typing import List, Dict, Any, Optional

from app.core.vector_store import vector_store
from app.core.embeddings import embedding_service

logger = logging.getLogger(__name__)


async def store_embeddings(
    ids: List[str],
    embeddings: List[List[float]],
    metadata: List[Dict[str, Any]]
) -> bool:
    """
    Store embeddings in vector database
    
    Args:
        ids: List of unique identifiers
        embeddings: List of embedding vectors
        metadata: List of metadata dictionaries
        
    Returns:
        True if successful
    """
    try:
        return await vector_store.store_embeddings(ids, embeddings, metadata)
    except Exception as e:
        logger.error(f"Error storing embeddings: {e}")
        return False


async def search_similar(
    query_embedding: List[float],
    top_k: int = 10,
    filters: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search for similar vectors
    
    Args:
        query_embedding: Query embedding vector
        top_k: Number of results to return
        filters: Optional metadata filters
        
    Returns:
        List of similar items with scores
    """
    try:
        return await vector_store.search_similar(query_embedding, top_k, filters)
    except Exception as e:
        logger.error(f"Error searching similar vectors: {e}")
        return []


async def search_hybrid(
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Hybrid search: generate embedding from query text and search
    
    Args:
        query: Text query
        filters: Optional metadata filters
        top_k: Number of results to return
        
    Returns:
        List of similar items with scores
    """
    try:
        # Generate embedding for the query
        query_embedding = await embedding_service.generate_embedding(query)
        
        # Search with the embedding
        return await vector_store.search_similar(query_embedding, top_k, filters)
    except Exception as e:
        logger.error(f"Error in hybrid search: {e}")
        return []


async def update_embeddings(
    ids: List[str],
    embeddings: List[List[float]],
    metadata: List[Dict[str, Any]]
) -> bool:
    """
    Update existing embeddings
    
    Args:
        ids: List of IDs to update
        embeddings: New embedding vectors
        metadata: New metadata
        
    Returns:
        True if successful
    """
    try:
        # In Qdrant, upsert handles both insert and update
        return await vector_store.store_embeddings(ids, embeddings, metadata)
    except Exception as e:
        logger.error(f"Error updating embeddings: {e}")
        return False


async def delete_embeddings(ids: List[str]) -> bool:
    """
    Delete embeddings by IDs
    
    Args:
        ids: List of IDs to delete
        
    Returns:
        True if successful
    """
    try:
        return await vector_store.delete_embeddings(ids)
    except Exception as e:
        logger.error(f"Error deleting embeddings: {e}")
        return False


async def get_stats() -> Dict[str, Any]:
    """
    Get vector database statistics
    
    Returns:
        Dictionary with collection statistics
    """
    try:
        return await vector_store.get_collection_stats()
    except Exception as e:
        logger.error(f"Error getting vector DB stats: {e}")
        return {}

