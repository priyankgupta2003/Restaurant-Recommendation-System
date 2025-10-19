"""
Script to ingest sample restaurant data into vector database
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.core.vector_store import vector_store
from app.core.embeddings import embedding_service
from app.mcp_server.client import mcp_client


async def ingest_data():
    """Ingest sample restaurant data"""
    print("Ingesting sample restaurant data...")
    
    try:
        # Initialize services
        await mcp_client.connect()
        await vector_store.initialize()
        
        # Sample locations to fetch restaurants from
        locations = [
            "San Francisco, CA",
            "New York, NY",
            "Los Angeles, CA",
            "Chicago, IL",
            "Austin, TX"
        ]
        
        all_restaurants = []
        
        for location in locations:
            print(f"\nFetching restaurants from {location}...")
            
            try:
                result = await mcp_client.search_restaurants(
                    location=location,
                    limit=50,
                    categories="restaurants"
                )
                
                businesses = result.get("businesses", [])
                print(f"  Found {len(businesses)} restaurants")
                all_restaurants.extend(businesses)
                
            except Exception as e:
                print(f"  Error fetching from {location}: {e}")
                continue
        
        if not all_restaurants:
            print("No restaurants fetched. Exiting.")
            return
        
        print(f"\nTotal restaurants to ingest: {len(all_restaurants)}")
        
        # Prepare data for vector DB
        ids = []
        texts = []
        metadata = []
        
        for restaurant in all_restaurants:
            restaurant_id = restaurant.get("id")
            if not restaurant_id:
                continue
            
            # Prepare text for embedding
            text = embedding_service.prepare_restaurant_text(restaurant)
            
            ids.append(restaurant_id)
            texts.append(text)
            metadata.append({
                "id": restaurant_id,
                "name": restaurant.get("name"),
                "rating": restaurant.get("rating"),
                "review_count": restaurant.get("review_count"),
                "price": restaurant.get("price"),
                "categories": [cat.get("title") for cat in restaurant.get("categories", [])],
                "location": restaurant.get("location", {}),
                "source": "yelp"
            })
        
        print(f"\nGenerating embeddings for {len(texts)} restaurants...")
        embeddings = await embedding_service.generate_embeddings(texts)
        
        print("Storing in vector database...")
        success = await mcp_client.store_embeddings(ids, embeddings, metadata)
        
        if success:
            print("✅ Data ingestion completed successfully!")
            
            # Get stats
            stats = await vector_store.get_collection_stats()
            print(f"\nVector DB Stats:")
            print(f"  - Total vectors: {stats.get('vectors_count', 0)}")
            print(f"  - Total points: {stats.get('points_count', 0)}")
        else:
            print("❌ Failed to store embeddings")
        
        await mcp_client.close()
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(ingest_data())

