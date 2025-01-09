from typing import Dict, Optional
import httpx
from fastapi import HTTPException
import logging
from pydantic import BaseModel
from app.config import settings

logger = logging.getLogger(__name__)

class CarrierInfo(BaseModel):
    legal_name: str
    dba_name: Optional[str] = None
    dot_number: Optional[str] = None
    status: str
    is_active: bool = False
    has_authority: bool = False
    has_insurance: bool = False

class CarrierService:
    def __init__(self):
        self.api_key = settings.FMCSA_API_KEY
        self.base_url = "https://mobile.fmcsa.dot.gov/qc/services/carriers"
        
    async def validate_carrier(self, mc_number: str) -> Dict:
        """
        Validates carrier using FMCSA API.
        Returns carrier details and validation status.
        """
        try:
            # Clean MC number format
            mc_number = mc_number.upper().replace("MC", "").strip()
            logger.info(f"Validating carrier MC#{mc_number}")

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/name/{mc_number}",
                    params={"webKey": self.api_key}
                )
                
                if response.status_code == 404:
                    logger.warning(f"Carrier MC#{mc_number} not found")
                    return {"is_valid": False, "error": "Carrier not found"}

                if response.status_code != 200:
                    logger.error(f"FMCSA API error: {response.status_code}")
                    raise HTTPException(status_code=500, detail="Error validating carrier")

                data = response.json()
                carriers = data.get("content", [])
                
                if not carriers:
                    logger.warning(f"No carrier found for MC#{mc_number}")
                    return {
                        "is_valid": False,
                        "error": "No carrier found"
                    }

                carrier_data = carriers[0].get("carrier", {})
                carrier_info = self._process_carrier(carrier_data)
                        
                return {
                    "is_valid": carrier_info.is_active and carrier_info.has_authority,
                    "carrier": carrier_info.dict(),
                    "message": "Carrier validated successfully"
                }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error validating carrier: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def _process_carrier(self, data: Dict) -> CarrierInfo:
        """Process raw carrier data into structured format"""
        return CarrierInfo(
            legal_name=data.get("legalName", "UNKNOWN"),
            dba_name=data.get("dbaName"),
            dot_number=str(data.get("dotNumber")) if data.get("dotNumber") else None,
            status=data.get("statusCode", "UNKNOWN"),
            is_active=data.get("statusCode") == "A",
            has_authority=data.get("commonAuthorityStatus") in ["A", "ACTIVE"],
            has_insurance=bool(data.get("bipdInsuranceOnFile"))
        )