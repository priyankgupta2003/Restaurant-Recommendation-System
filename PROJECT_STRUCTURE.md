# 📁 Project Structure

Complete overview of the Restaurant Recommendation System codebase.

## Directory Tree

```
Restaurant-Recommendation-System/
│
├── backend/                           # Backend application (Python/FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI entry point
│   │   ├── config.py                 # Configuration management
│   │   │
│   │   ├── api/                      # API layer
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── chat.py          # Chat endpoints
│   │   │       ├── restaurants.py    # Restaurant endpoints
│   │   │       └── health.py         # Health check endpoints
│   │   │
│   │   ├── core/                     # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── cache.py             # Redis cache manager
│   │   │   ├── embeddings.py        # Embedding generation
│   │   │   └── vector_store.py      # Vector DB client
│   │   │
│   │   ├── mcp_server/              # Unified MCP Server
│   │   │   ├── __init__.py
│   │   │   ├── client.py           # MCP client for FastAPI
│   │   │   └── tools/              # MCP tool modules
│   │   │       ├── __init__.py
│   │   │       ├── google_location.py   # Google Location tools
│   │   │       ├── google_search.py     # Google Search tools
│   │   │       ├── yelp_business.py     # Yelp Business tools
│   │   │       ├── yelp_reviews.py      # Yelp Reviews tools
│   │   │       └── vectordb.py          # Vector DB tools
│   │   │
│   │   ├── models/                  # Data models
│   │   │   ├── __init__.py
│   │   │   ├── chat.py             # Chat models
│   │   │   └── restaurant.py       # Restaurant models
│   │   │
│   │   ├── schemas/                # API schemas (Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── chat_schemas.py
│   │   │   └── restaurant_schemas.py
│   │   │
│   │   └── services/               # Business logic
│   │       ├── __init__.py
│   │       ├── chat_service.py     # Chat orchestration
│   │       ├── llm_service.py      # LLM integration
│   │       └── rag_service.py      # RAG pipeline
│   │
│   ├── scripts/                    # Utility scripts
│   │   ├── __init__.py
│   │   ├── setup_vectordb.py      # Initialize vector DB
│   │   └── ingest_sample_data.py  # Data ingestion
│   │
│   ├── tests/                      # Tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   │
│   ├── requirements.txt            # Python dependencies
│   ├── pyproject.toml             # Project metadata
│   └── README.md
│
├── frontend/                       # Frontend application (Next.js/React)
│   ├── src/
│   │   ├── app/                   # Next.js App Router
│   │   │   ├── layout.tsx         # Root layout
│   │   │   ├── page.tsx           # Home page
│   │   │   ├── providers.tsx      # React Query provider
│   │   │   └── globals.css        # Global styles
│   │   │
│   │   ├── components/            # React components
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInterface.tsx   # Main chat UI
│   │   │   │   ├── MessageList.tsx     # Message display
│   │   │   │   └── InputBox.tsx        # Input component
│   │   │   └── Restaurant/
│   │   │       ├── RestaurantCard.tsx  # Restaurant card
│   │   │       └── RestaurantList.tsx  # Restaurant grid
│   │   │
│   │   ├── hooks/                 # Custom React hooks
│   │   │   ├── useChat.ts        # Chat hook
│   │   │   └── useLocation.ts    # Location hook
│   │   │
│   │   ├── services/             # API services
│   │   │   └── api.ts            # Backend API client
│   │   │
│   │   └── types/                # TypeScript types
│   │       ├── chat.ts
│   │       └── restaurant.ts
│   │
│   ├── public/                   # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── README.md
│
├── docker/                       # Docker configurations
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── docker-compose.yml           # Docker Compose config
├── .gitignore
├── README.md                    # Main documentation
├── SETUP.md                     # Setup guide
└── PROJECT_STRUCTURE.md         # This file

```

## Key Components

### Backend

#### 1. **API Layer** (`app/api/`)
- **Purpose**: HTTP endpoint definitions
- **Key Files**:
  - `routes/chat.py`: Chat conversation endpoints
  - `routes/restaurants.py`: Restaurant search and details
  - `routes/health.py`: Health checks and monitoring

#### 2. **Core Utilities** (`app/core/`)
- **Purpose**: Fundamental services used across the app
- **Key Files**:
  - `cache.py`: Redis caching with decorator support
  - `embeddings.py`: Text embedding generation (OpenAI)
  - `vector_store.py`: Qdrant vector database client

#### 3. **MCP Server** (`app/mcp_server/`)
- **Purpose**: Unified Model Context Protocol server
- **Architecture**: Single server with domain-organized tools
- **Tools**:
  - Google Location: Geocoding, distance calculation
  - Google Search: Places search
  - Yelp Business: Restaurant search
  - Yelp Reviews: Review fetching
  - VectorDB: Embedding storage and search

#### 4. **Services** (`app/services/`)
- **Purpose**: Business logic and orchestration
- **Key Files**:
  - `chat_service.py`: Manages conversation flow
  - `llm_service.py`: LLM API integration (OpenAI/Anthropic)
  - `rag_service.py`: RAG pipeline implementation

#### 5. **Models & Schemas** (`app/models/`, `app/schemas/`)
- **Models**: Internal data structures
- **Schemas**: API request/response validation (Pydantic)

### Frontend

#### 1. **App Router** (`src/app/`)
- Next.js 14 App Router structure
- Server and client components
- Global layout and providers

#### 2. **Components** (`src/components/`)
- **Chat Components**:
  - `ChatInterface`: Main UI orchestrator
  - `MessageList`: Scrollable message display
  - `InputBox`: Message input with keyboard shortcuts
- **Restaurant Components**:
  - `RestaurantCard`: Individual restaurant display
  - `RestaurantList`: Grid layout of restaurants

#### 3. **Hooks** (`src/hooks/`)
- `useChat`: Chat state management and API calls
- `useLocation`: Geolocation handling

#### 4. **Services** (`src/services/`)
- `api.ts`: Axios-based API client with typed endpoints

## Data Flow

### Chat Request Flow

```
User Input (Frontend)
    ↓
useChat Hook
    ↓
API Service (Axios)
    ↓
FastAPI Backend (/api/v1/chat)
    ↓
Chat Service
    ↓
RAG Service
    ├→ MCP Client → Yelp API (Real-time data)
    └→ MCP Client → Vector DB (Semantic search)
    ↓
LLM Service (OpenAI/Anthropic)
    ↓
Response → Frontend
```

### RAG Pipeline Flow

```
User Query
    ↓
1. Intent Detection
   (Extract cuisine, price, location)
    ↓
2. Parallel Retrieval
   ├→ Yelp API Search (Real-time restaurants)
   └→ Vector DB Search (Semantic similarity)
    ↓
3. Merge & Rank Results
    ↓
4. Enrich with Reviews
    ↓
5. Build Context
    ↓
6. LLM Generation
    ↓
Formatted Response
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Python**: 3.11+
- **LLM**: OpenAI / Anthropic
- **Vector DB**: Qdrant
- **Cache**: Redis
- **HTTP Client**: httpx (async)

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **UI**: Tailwind CSS
- **State**: React Query + Zustand
- **HTTP**: Axios

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Reverse Proxy**: (Optional) Nginx

## Configuration Files

| File | Purpose |
|------|---------|
| `backend/.env` | Backend environment variables |
| `frontend/.env.local` | Frontend environment variables |
| `docker-compose.yml` | Multi-container orchestration |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |
| `backend/pyproject.toml` | Python project metadata |
| `frontend/tsconfig.json` | TypeScript configuration |
| `frontend/tailwind.config.js` | Tailwind CSS configuration |

## Environment Variables

### Backend
```
OPENAI_API_KEY          # OpenAI API key
GOOGLE_MAPS_API_KEY     # Google Maps key
YELP_API_KEY            # Yelp Fusion key
QDRANT_URL              # Vector DB URL
REDIS_HOST              # Redis host
```

### Frontend
```
NEXT_PUBLIC_API_URL             # Backend API URL
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY # Google Maps key (client-side)
```

## Adding New Features

### Adding a New MCP Tool

1. Create tool file in `backend/app/mcp_server/tools/`
2. Implement tool functions with proper typing
3. Import in `tools/__init__.py`
4. Add convenience methods in `client.py`

### Adding a New API Endpoint

1. Create route in `backend/app/api/routes/`
2. Define schemas in `backend/app/schemas/`
3. Implement service logic in `backend/app/services/`
4. Include router in `main.py`

### Adding a New Frontend Component

1. Create component in `frontend/src/components/`
2. Add types in `frontend/src/types/`
3. Create hook if needed in `frontend/src/hooks/`
4. Use in pages/components

## Testing Structure

### Backend Tests
```
tests/
├── unit/
│   ├── test_chat_service.py
│   ├── test_rag_service.py
│   └── test_mcp_tools.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_mcp_integration.py
└── conftest.py
```

### Frontend Tests
```
__tests__/
├── components/
├── hooks/
└── services/
```

## Performance Considerations

- **Caching**: Redis for API responses and geocoding
- **Async**: All I/O operations are async
- **Connection Pooling**: HTTP clients use connection pools
- **Rate Limiting**: Implemented per API provider
- **Vector Search**: Optimized with metadata filtering

## Security Considerations

- API keys in environment variables (never committed)
- CORS configured for specific origins
- Input validation with Pydantic
- Rate limiting on endpoints
- Secure WebSocket connections (if implemented)

---

For detailed setup instructions, see [SETUP.md](SETUP.md).
For API documentation, run the backend and visit http://localhost:8000/docs.

