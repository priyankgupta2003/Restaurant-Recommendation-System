# ⚡ Quick Start Guide

Get the Restaurant Recommendation System running in under 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Docker installed (recommended)
- [ ] API Keys obtained (see below)

## Get Your API Keys (5 minutes)

### Required Keys

1. **OpenAI API Key** 
   - Visit: https://platform.openai.com/api-keys
   - Sign up → Create API key
   - Copy key (starts with `sk-`)

2. **Yelp API Key**
   - Visit: https://www.yelp.com/developers
   - Create App → Copy API Key

3. **Google Maps API Key**
   - Visit: https://console.cloud.google.com/
   - Enable: Geocoding API, Places API
   - Credentials → Create API Key

## Option 1: Docker (Recommended) ⚡

### 1. Clone and Configure
```bash
git clone <repo-url>
cd Restaurant-Recommendation-System

# Create backend .env
cat > backend/.env << EOF
OPENAI_API_KEY=your-openai-key
YELP_API_KEY=your-yelp-key
GOOGLE_MAPS_API_KEY=your-google-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
VECTOR_DB_TYPE=qdrant
QDRANT_URL=http://qdrant:6333
REDIS_HOST=redis
EOF

# Create frontend .env.local
cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-key
EOF
```

### 2. Start Everything
```bash
docker-compose up -d
```

### 3. Wait for Services (30-60 seconds)
```bash
# Check status
docker-compose ps

# Watch logs
docker-compose logs -f
```

### 4. Initialize Vector Database
```bash
docker-compose exec backend python scripts/setup_vectordb.py
```

### 5. (Optional) Load Sample Data
```bash
docker-compose exec backend python scripts/ingest_sample_data.py
```

### 6. Open Application
- Frontend: http://localhost:3000
- Backend API Docs: http://localhost:8000/docs

## Option 2: Manual Setup 🔧

### Backend (Terminal 1)

```bash
# 1. Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# 4. Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 5. Initialize Vector DB
python scripts/setup_vectordb.py

# 6. Run Backend
python -m app.main
```

### Frontend (Terminal 2)

```bash
# 1. Setup
cd frontend
npm install

# 2. Configure
cp .env.example .env.local
# Edit .env.local with your API URL

# 3. Run Frontend
npm run dev
```

## First Steps

### 1. Test the Application

Open http://localhost:3000

1. Click "Get Location" button (or skip)
2. Type: `Find me Italian restaurants in San Francisco`
3. Wait for AI response and restaurant cards

### 2. Verify Backend

Visit http://localhost:8000/docs

Try the health check:
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "mcp_server": "healthy",
    "cache": "healthy",
    "vector_db": "healthy"
  }
}
```

## Common Issues & Solutions

### "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:8000/api/v1/health

# Check docker containers
docker-compose ps
```

### "OpenAI API Error"
```bash
# Verify API key in backend/.env
grep OPENAI_API_KEY backend/.env

# Test key manually
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer your-key"
```

### "Redis connection failed"
```bash
# Check Redis is running
docker ps | grep redis

# Test connection
redis-cli ping  # Should return "PONG"
```

### "Qdrant connection failed"
```bash
# Check Qdrant is running
curl http://localhost:6333/collections

# Restart if needed
docker restart restaurant-qdrant
```

## Try These Queries

Once running, try these in the chat:

1. **Basic Search**
   - "Find me Italian restaurants"
   - "Show me pizza places nearby"

2. **With Filters**
   - "Best rated sushi restaurants under $30"
   - "Cheap Mexican food with vegetarian options"

3. **Location Specific**
   - "Italian restaurants in New York"
   - "Best brunch spots in San Francisco"

4. **Follow-up Questions**
   - "Tell me more about the first one"
   - "Any vegan options?"
   - "What about outdoor seating?"

## Next Steps

1. **Load More Data**
   ```bash
   python backend/scripts/ingest_sample_data.py
   ```

2. **Customize UI**
   - Edit `frontend/tailwind.config.js` for colors
   - Modify components in `frontend/src/components/`

3. **Add Features**
   - See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture
   - Check [README.md](README.md) for detailed docs

4. **Deploy to Production**
   - See [SETUP.md](SETUP.md) for deployment guide

## Performance Tips

### Speed Up Responses
1. **Reduce search limit** in backend/.env:
   ```env
   DEFAULT_SEARCH_LIMIT=10
   ```

2. **Enable caching** (already enabled):
   - Results cached for 1 hour
   - Geocoding cached for 24 hours

3. **Use faster LLM model**:
   ```env
   LLM_MODEL=gpt-3.5-turbo  # Faster than gpt-4
   ```

### Reduce API Costs
1. **Use caching** (enabled by default)
2. **Limit search results**
3. **Reduce embedding dimensions** (if using custom embeddings)

## Stopping Services

### Docker
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Manual
```bash
# Stop backend: Ctrl+C in terminal
# Stop frontend: Ctrl+C in terminal
# Stop Redis: docker stop <redis-container-id>
# Stop Qdrant: docker stop <qdrant-container-id>
```

## Getting Help

1. **Check logs**
   ```bash
   # Docker
   docker-compose logs backend
   docker-compose logs frontend
   
   # Manual
   # Check terminal output
   ```

2. **Health Check**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

3. **Documentation**
   - [README.md](README.md) - Overview
   - [SETUP.md](SETUP.md) - Detailed setup
   - [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Code structure

4. **API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Redis running on port 6379
- [ ] Qdrant running on port 6333
- [ ] Health check returns "healthy"
- [ ] Can send chat messages
- [ ] Restaurants appear in results
- [ ] Location detection works

## Congratulations! 🎉

You now have a fully functional AI-powered restaurant recommendation system!

---

**Need more help?** Check [SETUP.md](SETUP.md) for detailed instructions.

