"""
Script to initialize and set up the vector database
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.core.vector_store import vector_store


async def setup():
    """Initialize vector database collection"""
    print("Setting up vector database...")
    print(f"Vector DB Type: {settings.vector_db_type}")
    print(f"Collection: {settings.qdrant_collection}")
    
    try:
        # Initialize vector store
        await vector_store.initialize()
        print("✅ Vector database initialized successfully!")
        
        # Get stats
        stats = await vector_store.get_collection_stats()
        print(f"\nCollection Stats:")
        print(f"  - Vectors: {stats.get('vectors_count', 0)}")
        print(f"  - Points: {stats.get('points_count', 0)}")
        print(f"  - Status: {stats.get('status', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Error setting up vector database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(setup())

