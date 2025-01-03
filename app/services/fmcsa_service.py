from typing import Dict
import httpx
import logging
from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CarrierValidationResponse(BaseModel):
    legal_name: str
    dot_number: str | None = None
    status: str
    is_valid: bool

class FMCSAService:
    def __init__(self):
        self.api_key = "cdc33e44d693a3a58451898d4ec9df862c65b954"
        self.base_url = "https://mobile.fmcsa.dot.gov/qc/services"
        
    async def validate_carrier(self, mc_number: str) -> Dict:
        try:
            # Clean MC number
            mc_number = mc_number.upper().replace("MC", "").strip()
            logger.debug(f"Validating carrier: {mc_number}")
            
            async with httpx.AsyncClient() as client:
                # Use name search which seems more reliable
                url = f"{self.base_url}/carriers/name/{mc_number}"
                logger.debug(f"Request URL: {url}")
                
                response = await client.get(
                    url,
                    params={"webKey": self.api_key}
                )
                
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response body: {response.text}")

                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Carrier not found")

                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="FMCSA API error")

                data = response.json()
                carriers = data.get("content", [])
                
                if not carriers:
                    raise HTTPException(status_code=404, detail="No carrier found")

                # Take first match
                carrier = carriers[0].get("carrier", {})
                if not carrier:
                    raise HTTPException(status_code=404, detail="Invalid carrier data")

                return self._process_carrier_data(carrier)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail="Error validating carrier")

    def _process_carrier_data(self, carrier: Dict) -> Dict:
        status = carrier.get("statusCode", "UNKNOWN")
        is_valid = (
            carrier.get("allowedToOperate") == "Y" and
            status == "A"
        )
        
        return {
            "legal_name": carrier.get("legalName", "UNKNOWN"),
            "dot_number": str(carrier.get("dotNumber")) if carrier.get("dotNumber") else None,
            "status": status,
            "is_valid": is_valid
        }