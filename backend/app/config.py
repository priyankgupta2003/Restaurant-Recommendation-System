"""Application configuration management"""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "Restaurant-Recommendation-System"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_url: str = "http://localhost:3000"
    
    # API Keys
    openai_api_key: str = Field(default="")
    anthropic_api_key: str = Field(default="")
    google_maps_api_key: str = Field(default="")
    google_search_api_key: str = Field(default="")
    yelp_api_key: str = Field(default="")
    
    # LLM Configuration
    llm_provider: Literal["openai", "anthropic"] = "openai"
    llm_model: str = "gpt-4-turbo-preview"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    
    # Embeddings
    embedding_model: str = "text-embedding-3-large"
    embedding_dimension: int = 1536
    
    # Vector Database
    vector_db_type: Literal["qdrant", "pinecone"] = "qdrant"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = Field(default="")
    qdrant_collection: str = "restaurants"
    pinecone_api_key: str = Field(default="")
    pinecone_environment: str = "us-east-1-aws"
    pinecone_index: str = "restaurants"
    
    # Redis Cache
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = Field(default="")
    redis_db: int = 0
    cache_ttl: int = 3600
    
    # MCP Server Configuration
    mcp_server_name: str = "restaurant-recommendation-mcp"
    mcp_server_version: str = "1.0.0"
    mcp_timeout: int = 30
    mcp_max_retries: int = 3
    
    # Rate Limiting
    yelp_rate_limit: int = 5000
    google_rate_limit: int = 10000
    rate_limit_per_minute: int = 60
    
    # Search Configuration
    default_search_radius: int = 5000  # meters
    default_search_limit: int = 20
    max_restaurants_return: int = 10
    
    @property
    def redis_url(self) -> str:
        """Construct Redis URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


# Global settings instance
settings = Settings()

