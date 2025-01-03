from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from app.services.fmcsa_service import FMCSAService, CarrierValidationResponse
from app.core.dependencies import get_fmcsa_service

router = APIRouter()

@router.get("/validate", response_model=CarrierValidationResponse)
async def validate_carrier_get(
    mc_number: str,
    fmcsa_service: FMCSAService = Depends(get_fmcsa_service)
) -> Dict:
    return await fmcsa_service.validate_carrier(mc_number)

@router.post("/validate")
async def validate_carrier_post(
    mc_number: str,
    fmcsa_service: FMCSAService = Depends(get_fmcsa_service)
) -> Dict:
    return await fmcsa_service.validate_carrier(mc_number)