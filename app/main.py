from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import loads, carriers
from .core.cache import setup_cache
from .core.logging import LoggingMiddleware
from .core.security import verify_api_key
import uvicorn
from .config import settings

app = FastAPI(title="Load Checker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(
    loads.router, 
    prefix="/loads", 
    tags=["loads"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    carriers.router, 
    prefix="/carriers", 
    tags=["carriers"],
    dependencies=[Depends(verify_api_key)]
)

@app.on_event("startup")
async def startup_event():
    await setup_cache()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)