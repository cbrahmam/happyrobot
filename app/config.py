from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    API_KEY: str = os.getenv("API_KEY", "default_key")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379")
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "100"))
    CACHE_EXPIRATION: int = int(os.getenv("CACHE_EXPIRATION", "300"))
    FMCSA_API_KEY: str = os.getenv("FMCSA_API_KEY", "default_fmcsa_key")
    USE_HTTPS: bool = os.getenv("USE_HTTPS", "false").lower() == "true"

settings = Settings()