from typing import Dict, Optional
import httpx
from fastapi import HTTPException
import logging
from pydantic import BaseModel

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
        self.api_key = "cdc33e44d693a3a58451898d4ec9df862c65b954"
        self.base_url = "https://mobile.fmcsa.dot.gov/qc/services/carriers"
        
    async def validate_carrier(self, mc_number: str) -> Dict:
        """
        Validates carrier and checks if it matches ABC Trucking.
        Returns carrier details and validation status.
        """
        try:
            # Clean MC number format
            mc_number = mc_number.upper().replace("MC", "").strip()
            logger.info(f"Validating carrier MC#{mc_number}")

            async with httpx.AsyncClient() as client:
                # Fetch carrier data
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
                
                # Process each carrier match
                for carrier_data in carriers:
                    carrier = carrier_data.get("carrier", {})
                    carrier_info = self._process_carrier(carrier)
                    
                    # Check if this is ABC Trucking
                    if carrier_info.legal_name == "ABC TRUCKING" or carrier_info.dba_name == "ABC TRUCKING":
                        logger.info(f"Found ABC Trucking match for MC#{mc_number}")
                        return {
                            "is_valid": True,
                            "carrier": carrier_info.dict(),
                            "message": "Carrier validated successfully"
                        }

                logger.warning(f"No ABC Trucking match found for MC#{mc_number}")
                return {
                    "is_valid": False,
                    "error": "Not ABC Trucking",
                    "carriers_found": len(carriers)
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