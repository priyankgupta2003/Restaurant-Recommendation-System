"""Vector database client for semantic search"""

import logging
from typing import List, Dict, Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    Range
)

from app.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Vector database client for storing and searching embeddings"""
    
    def __init__(self):
        self.client: Optional[AsyncQdrantClient] = None
        self.collection_name = settings.qdrant_collection
        self.dimension = settings.embedding_dimension
        self._initialized = False
    
    async def initialize(self):
        """Initialize Qdrant client and create collection if needed"""
        try:
            self.client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key if settings.qdrant_api_key else None
            )
            
            # Check if collection exists
            collections = await self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE
                    )
                )
            
            self._initialized = True
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    async def store_embeddings(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        metadata: List[Dict[str, Any]]
    ) -> bool:
        """
        Store embeddings with metadata
        
        Args:
            ids: List of unique IDs
            embeddings: List of embedding vectors
            metadata: List of metadata dictionaries
            
        Returns:
            True if successful
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            points = [
                PointStruct(
                    id=id_,
                    vector=embedding,
                    payload=meta
                )
                for id_, embedding, meta in zip(ids, embeddings, metadata)
            ]
            
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Stored {len(points)} embeddings successfully")
            return True
        except Exception as e:
            logger.error(f"Error storing embeddings: {e}")
            return False
    
    async def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors
        
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of search results with scores and metadata
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Build filter if provided
            search_filter = None
            if filters:
                search_filter = self._build_filter(filters)
            
            results = await self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter
            )
            
            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "metadata": result.payload
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []
    
    async def delete_embeddings(self, ids: List[str]) -> bool:
        """
        Delete embeddings by IDs
        
        Args:
            ids: List of IDs to delete
            
        Returns:
            True if successful
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=ids
            )
            logger.info(f"Deleted {len(ids)} embeddings")
            return True
        except Exception as e:
            logger.error(f"Error deleting embeddings: {e}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        if not self._initialized:
            await self.initialize()
        
        try:
            info = await self.client.get_collection(self.collection_name)
            return {
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    @staticmethod
    def _build_filter(filters: Dict[str, Any]) -> Filter:
        """Build Qdrant filter from dictionary"""
        conditions = []
        
        for key, value in filters.items():
            if isinstance(value, dict):
                # Range filter (e.g., {"gte": 4.0})
                if "gte" in value or "lte" in value:
                    conditions.append(
                        FieldCondition(
                            key=key,
                            range=Range(
                                gte=value.get("gte"),
                                lte=value.get("lte")
                            )
                        )
                    )
            else:
                # Exact match filter
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
        
        return Filter(must=conditions) if conditions else None


# Global vector store instance
vector_store = VectorStore()

