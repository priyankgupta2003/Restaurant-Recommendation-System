# Restaurant Recommendation System - Backend

A Real-Time Restaurant Recommendation System using RAG (Retrieval-Augmented Generation) and Model Context Protocol (MCP).

## Features

- 🤖 **Unified MCP Server** - Single server with all API integrations (Google, Yelp, VectorDB)
- 🔍 **RAG Pipeline** - Semantic search + real-time data retrieval
- 💬 **Conversational AI** - Natural language restaurant recommendations
- 🗺️ **Location-Based** - Google Location API integration
- ⭐ **Rich Data** - Yelp reviews, ratings, menus
- 🚀 **High Performance** - Async FastAPI + Redis caching
- 📊 **Vector Database** - Qdrant for semantic search

## Architecture

```
FastAPI Backend
├── MCP Unified Server
│   ├── Google Location Tools
│   ├── Google Search Tools
│   ├── Yelp Business Tools
│   ├── Yelp Reviews Tools
│   └── Vector DB Tools
├── RAG Service
├── LLM Service (OpenAI/Anthropic)
├── Chat Orchestration
└── REST API Endpoints
```

## Prerequisites

- Python 3.11+
- Redis
- Qdrant (or Pinecone)
- API Keys:
  - OpenAI or Anthropic
  - Google Maps API
  - Google Search API (optional)
  - Yelp Fusion API

## Installation

1. **Clone the repository**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Start Redis** (if not using Docker)
```bash
redis-server
```

6. **Start Qdrant** (if not using Docker)
```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Running the Application

### Development Mode

```bash
python -m app.main
```

Or with uvicorn:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
- `GET /health` - Application health status
- `GET /readiness` - Readiness check
- `GET /liveness` - Liveness check

### Chat
- `POST /api/v1/chat` - Send a chat message
- `GET /api/v1/chat/session/{session_id}` - Get session history
- `DELETE /api/v1/chat/session/{session_id}` - Clear session

### Restaurants
- `POST /api/v1/restaurants/search` - Search restaurants
- `GET /api/v1/restaurants/{restaurant_id}` - Get restaurant details
- `GET /api/v1/restaurants/nearby` - Get nearby restaurants

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

Edit `.env` file to configure:

```env
# LLM Provider
LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4-turbo-preview

# Vector Database
VECTOR_DB_TYPE=qdrant  # or pinecone
QDRANT_URL=http://localhost:6333

# Cache
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core utilities (cache, vector store, embeddings)
│   ├── mcp_server/       # Unified MCP server
│   │   ├── client.py     # MCP client
│   │   └── tools/        # Tool modules
│   ├── models/           # Data models
│   ├── schemas/          # API schemas
│   ├── services/         # Business logic
│   ├── config.py         # Configuration
│   └── main.py           # Application entry point
├── tests/                # Tests
├── scripts/              # Utility scripts
└── requirements.txt      # Dependencies
```

## MCP Tool Catalog

### Google Location Tools
- `geocode(address)` - Convert address to coordinates
- `reverse_geocode(lat, lng)` - Convert coordinates to address
- `calculate_distance()` - Calculate distance between points

### Yelp Tools
- `search_businesses()` - Search restaurants
- `get_business()` - Get business details
- `get_reviews()` - Get reviews

### Vector DB Tools
- `store_embeddings()` - Store embeddings
- `search_similar()` - Semantic search
- `search_hybrid()` - Hybrid search

## Example Usage

### Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me the best Italian restaurants in San Francisco",
    "location": {"address": "San Francisco, CA"}
  }'
```

### Search Restaurants

```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "pizza",
    "location": "New York, NY",
    "price": "1,2",
    "limit": 10
  }'
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chat_service.py
```

## Development

### Code Formatting

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

## Troubleshooting

### MCP Client Connection Issues
- Ensure all API keys are set in `.env`
- Check that services (Redis, Qdrant) are running

### Vector Database Issues
- Initialize Qdrant collection: Run `scripts/setup_vectordb.py`
- Check Qdrant is accessible at configured URL

### Cache Issues
- Verify Redis is running: `redis-cli ping`
- Check Redis connection in health endpoint

## Contributing

1. Create a feature branch
2. Make changes
3. Run tests and linting
4. Submit pull request

## License

MIT License

