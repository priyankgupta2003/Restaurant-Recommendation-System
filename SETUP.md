# 📋 Setup Guide

Complete setup guide for the Restaurant Recommendation System.

## Table of Contents
1. [API Keys Setup](#api-keys-setup)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Data Ingestion](#data-ingestion)
5. [Troubleshooting](#troubleshooting)

## API Keys Setup

### 1. OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy the key (starts with `sk-`)

### 2. Google Maps API Key
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable these APIs:
   - Geocoding API
   - Places API
   - Maps JavaScript API
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key

### 3. Yelp Fusion API Key
1. Go to https://www.yelp.com/developers
2. Sign up or log in
3. Create a new app
4. Copy the API Key from your app dashboard

### 4. Anthropic API Key (Optional)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create and copy the key

## Development Setup

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
```

5. **Edit .env file with your API keys**
```env
# LLM
OPENAI_API_KEY=sk-your-openai-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# Google
GOOGLE_MAPS_API_KEY=your-google-maps-key
GOOGLE_SEARCH_API_KEY=your-google-search-key

# Yelp
YELP_API_KEY=your-yelp-key

# Vector DB
VECTOR_DB_TYPE=qdrant
QDRANT_URL=http://localhost:6333

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

6. **Start Redis**
```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally
# macOS: brew install redis && redis-server
# Ubuntu: sudo apt install redis-server && redis-server
# Windows: Use Docker
```

7. **Start Qdrant**
```bash
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

8. **Initialize vector database**
```bash
python scripts/setup_vectordb.py
```

9. **Run the backend**
```bash
python -m app.main
```

Backend should now be running at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create .env.local file**
```bash
cp .env.example .env.local
```

4. **Edit .env.local**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-key
```

5. **Run the frontend**
```bash
npm run dev
```

Frontend should now be running at http://localhost:3000

## Production Deployment

### Using Docker Compose

1. **Clone repository**
```bash
git clone <your-repo-url>
cd Restaurant-Recommendation-System
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env

# Frontend
cp frontend/.env.example frontend/.env.local
# Edit frontend/.env.local
```

3. **Build and start services**
```bash
docker-compose up -d
```

4. **Check logs**
```bash
docker-compose logs -f
```

5. **Stop services**
```bash
docker-compose down
```

### Manual Production Deployment

#### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend

```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start
```

## Data Ingestion

After setting up the backend, ingest restaurant data:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Run data ingestion script
python scripts/ingest_sample_data.py
```

This will:
1. Fetch restaurants from multiple cities via Yelp API
2. Generate embeddings using OpenAI
3. Store in Qdrant vector database

**Note**: This may take 10-15 minutes and will use your API quotas.

## Verification

### 1. Check Backend Health
```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "mcp_server": "healthy",
    "cache": "healthy",
    "vector_db": "healthy"
  }
}
```

### 2. Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me Italian restaurants",
    "location": {"address": "San Francisco, CA"}
  }'
```

### 3. Open Frontend
Navigate to http://localhost:3000 and try:
- Click "Get Location" button
- Type: "Find me the best pizza places nearby"
- Check if restaurants appear on the right side

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

**Problem**: Redis connection error
```bash
# Solution: Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Or check if Redis is running
redis-cli ping  # Should return "PONG"
```

**Problem**: Qdrant connection error
```bash
# Solution: Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Verify it's running
curl http://localhost:6333/collections
```

**Problem**: API key errors
```bash
# Solution: Verify API keys in .env
# - OpenAI key starts with 'sk-'
# - Yelp key is a long alphanumeric string
# - Google key can be any format
```

### Frontend Issues

**Problem**: Cannot connect to backend
```bash
# Solution: Check NEXT_PUBLIC_API_URL in .env.local
# Ensure backend is running on the correct port
curl http://localhost:8000/api/v1/health
```

**Problem**: Location not working
```
Solution:
1. Ensure HTTPS (or use localhost)
2. Check browser location permissions
3. Verify Google Maps API key
```

**Problem**: Build errors
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

### Docker Issues

**Problem**: Container won't start
```bash
# Solution: Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Problem**: Port already in use
```bash
# Solution: Change ports in docker-compose.yml
# Or stop conflicting services
```

## Performance Tuning

### Backend

1. **Increase workers**
```bash
uvicorn app.main:app --workers 4
```

2. **Adjust cache TTL** (in .env)
```env
CACHE_TTL=7200  # 2 hours
```

3. **Optimize vector search**
```env
DEFAULT_SEARCH_LIMIT=10  # Reduce for faster search
```

### Frontend

1. **Enable output standalone** (next.config.js)
```javascript
output: 'standalone'
```

2. **Optimize images**
- Use Next.js Image component
- Configure image domains in next.config.js

## Next Steps

1. **Customize the UI** - Edit Tailwind config and components
2. **Add authentication** - Implement user accounts
3. **Add favorites** - Let users save restaurants
4. **Implement ratings** - Allow users to rate recommendations
5. **Add more data sources** - Integrate additional APIs

## Support

If you encounter issues:
1. Check the logs
2. Review this guide
3. Check the main README.md
4. Open an issue on GitHub

---

Happy coding! 🚀

