# 🍽️ Restaurant Recommendation System

A Real-Time Restaurant Recommendation System powered by RAG (Retrieval-Augmented Generation) and Model Context Protocol (MCP).

## 🌟 Features

- **🤖 AI-Powered Recommendations** - Natural language conversational interface
- **🔌 Unified MCP Server** - Single server integrating Google Maps, Yelp, and Vector DB
- **🔍 RAG Pipeline** - Combines semantic search with real-time API data
- **📍 Location-Based** - Google Location API for accurate positioning
- **⭐ Rich Restaurant Data** - Reviews, ratings, menus, and photos from Yelp
- **💾 Vector Database** - Semantic search using Qdrant
- **⚡ High Performance** - Async FastAPI backend with Redis caching
- **🎨 Modern UI** - Beautiful Next.js frontend with Tailwind CSS

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js + React)                   │
│              Chat Interface | Restaurant Display                 │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
┌────────────────────────────▼────────────────────────────────────┐
│                     Backend (FastAPI)                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Chat Service | RAG Pipeline | LLM Service              │  │
│  └────────────────────────┬─────────────────────────────────┘  │
└───────────────────────────┼─────────────────────────────────────┘
                            │ MCP Protocol
┌───────────────────────────▼─────────────────────────────────────┐
│              UNIFIED MCP SERVER                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Google Location | Yelp Business | Vector DB Tools      │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
         │              │              │
    ┌────▼────┐    ┌────▼────┐   ┌────▼─────┐
    │ Google  │    │  Yelp   │   │  Qdrant  │
    │   API   │    │   API   │   │ VectorDB │
    └─────────┘    └─────────┘   └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose** (recommended)
- **API Keys**:
  - OpenAI or Anthropic
  - Google Maps API
  - Yelp Fusion API

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd Restaurant-Recommendation-System
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Frontend
cp frontend/.env.example frontend/.env.local
# Edit frontend/.env.local with your configuration
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Start Redis
redis-server

# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Run backend
python -m app.main
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local

# Run development server
npm run dev
```

## 📖 Documentation

### Backend Documentation
- [Backend README](backend/README.md)
- API Documentation: http://localhost:8000/docs (when running)

### Frontend Documentation
- [Frontend README](frontend/README.md)

## 🛠️ Configuration

### Backend (.env)

```env
# LLM Provider
OPENAI_API_KEY=sk-your-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# Google APIs
GOOGLE_MAPS_API_KEY=your-key
GOOGLE_SEARCH_API_KEY=your-key

# Yelp API
YELP_API_KEY=your-key

# Vector Database
VECTOR_DB_TYPE=qdrant
QDRANT_URL=http://localhost:6333

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-key
```

## 📚 API Endpoints

### Chat
- `POST /api/v1/chat` - Send chat message
- `GET /api/v1/chat/session/{session_id}` - Get session
- `DELETE /api/v1/chat/session/{session_id}` - Clear session

### Restaurants
- `POST /api/v1/restaurants/search` - Search restaurants
- `GET /api/v1/restaurants/{id}` - Get details
- `GET /api/v1/restaurants/nearby` - Get nearby

### Health
- `GET /api/v1/health` - Health check
- `GET /api/v1/readiness` - Readiness probe
- `GET /api/v1/liveness` - Liveness probe

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run type-check
```

## 🔧 Development

### Backend Development
```bash
cd backend
source venv/bin/activate

# Format code
black app/

# Lint
ruff check app/

# Type check
mypy app/
```

### Frontend Development
```bash
cd frontend

# Lint
npm run lint

# Type check
npm run type-check
```

## 📦 Project Structure

```
Restaurant-Recommendation-System/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core utilities
│   │   ├── mcp_server/   # Unified MCP server
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── main.py       # Entry point
│   └── requirements.txt
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # Pages
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   └── services/    # API services
│   └── package.json
├── docker/              # Docker configurations
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker-compose.yml   # Docker Compose config
└── README.md
```

## 🎯 Usage Examples

### Example 1: Basic Search
```
User: "Find me Italian restaurants in San Francisco"
AI: [Returns top Italian restaurants with details]
```

### Example 2: Specific Requirements
```
User: "I need a vegan-friendly restaurant with outdoor seating, under $30"
AI: [Returns filtered recommendations matching criteria]
```

### Example 3: Follow-up Questions
```
User: "Tell me more about the first restaurant"
AI: [Provides detailed information about that specific restaurant]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Backend Issues
- **MCP Connection Failed**: Check API keys in `.env`
- **Redis Connection Error**: Ensure Redis is running
- **Vector DB Error**: Verify Qdrant is accessible

### Frontend Issues
- **API Connection Failed**: Check `NEXT_PUBLIC_API_URL`
- **Location Not Working**: Verify HTTPS or localhost
- **CORS Error**: Check backend CORS configuration

## 📄 License

MIT License

## 🙏 Acknowledgments

- OpenAI / Anthropic for LLM APIs
- Yelp for restaurant data
- Google Maps for location services
- Qdrant for vector database
- FastAPI and Next.js communities

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using RAG and MCP**

