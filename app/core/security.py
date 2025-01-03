from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings
import ssl
import certifi

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    return api_key

def get_ssl_context():
    context = ssl.create_default_context(cafile=certifi.where())
    context.load_cert_chain(
        settings.SSL_CERT_PATH,
        settings.SSL_KEY_PATH
    )
    return context