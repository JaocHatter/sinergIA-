from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from groq import Groq
from openai import OpenAI

class Settings(BaseSettings):
    """Application settings with validation using Pydantic"""
    # API Keys and Credentials
    openai_api_key: str
    groq_api_key: str
    # Research Configuration
    max_search_results: int = Field(default=5, ge=1)
    max_scrape_retries: int = Field(default=3, ge=1)
    research_timeout: int = Field(default=300, ge=60)  # minimum 60 seconds
        
    # Model Configuration
    gpt_model: str = Field(default="gpt-4o-mini")
    groq_model: str = Field(default="llama-3.2-11b-text-preview")
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    
    # Neo4j DB configuration
    username: str
    password: str
    url: str 

    # Embedding
    openai_endpoint: str = Field(default= "https://api.openai.com/v1/embeddings")
    embed_model: str = Field(default= "text-embedding-ada-002")

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Create settings instance
settings = Settings()

# Make variables available at module level for backward compatibility
OPENAI_API_KEY = settings.openai_api_key
GROQ_API_KEY = settings.groq_api_key
OPENAI_ENDPOINT = settings.openai_endpoint
MAX_SEARCH_RESULTS = settings.max_search_results
MAX_SCRAPE_RETRIES = settings.max_scrape_retries
RESEARCH_TIMEOUT = settings.research_timeout
GPT_MODEL = settings.gpt_model
TEMPERATURE = settings.temperature
LOG_LEVEL = settings.log_level
USERNAME = settings.username
PASSWORD = settings.password
URL = settings.url

client_groq = Groq(api_key = settings.groq_api_key)
client_openai = OpenAI(api_key= settings.openai_api_key)