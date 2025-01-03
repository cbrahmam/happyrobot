import logging
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.utcnow()
        response = None
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise e
        finally:
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds() * 1000
            logger.info(
                f"Path: {request.url.path} "
                f"Duration: {duration:.2f}ms "
                f"Status: {response.status_code if response else 'Failed'}"
            )