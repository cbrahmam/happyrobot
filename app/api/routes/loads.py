from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from app.services.load_service import LoadService
from app.core.dependencies import get_load_service
from app.core.security import verify_api_key

router = APIRouter()

@router.get("/check", response_model=Dict)
async def get_load_get(
    reference_number: str,
    api_key: str = Depends(verify_api_key),
    load_service: LoadService = Depends(get_load_service)
) -> Dict:
    reference_number = reference_number.upper().strip().replace(" ", "")
    return await load_service.get_load(reference_number)

@router.post("/check")
async def get_load_post(
    reference_number: str,
    api_key: str = Depends(verify_api_key),
    load_service: LoadService = Depends(get_load_service)
) -> Dict:
    reference_number = reference_number.upper().strip().replace(" ", "")
    return await load_service.get_load(reference_number)