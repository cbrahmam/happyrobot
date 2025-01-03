from pydantic import BaseModel, Field
from typing import Optional, List, Union

class LoadResponse(BaseModel):
    reference_number: str = Field(..., description="Unique identifier for the load")
    origin: str = Field(..., description="Starting location")
    destination: str = Field(..., description="Final destination")
    equipment_type: str = Field(..., description="Type of equipment required")
    rate: Union[float, None] = Field(None, description="Rate for the load")
    commodity: str = Field(..., description="Type of goods being transported")
    weight: Optional[float] = Field(None, description="Weight of the load in pounds")
    pickup_date: Optional[str] = Field(None, description="Scheduled pickup date/time")
    delivery_date: Optional[str] = Field(None, description="Expected delivery date/time")
    special_requirements: Optional[List[str]] = Field(default=[], description="Special requirements for the load")
    temperature: Optional[float] = Field(None, description="Required temperature for reefer loads")
    length_required: Optional[float] = Field(None, description="Minimum trailer length required")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "reference_number": "LOAD123",
                "origin": "Chicago, IL",
                "destination": "Dallas, TX",
                "equipment_type": "Dry Van",
                "rate": 2500.00,
                "commodity": "General Merchandise",
                "weight": 42000.0,
                "pickup_date": "2024-12-25 08:00:00",
                "delivery_date": "2024-12-26 16:00:00",
                "special_requirements": ["TWIC", "Load Bars"],
                "temperature": None,
                "length_required": 53.0
            }
        }

class LoadSearch(BaseModel):
    origin: Optional[str] = Field(None, description="Origin city/state")
    destination: Optional[str] = Field(None, description="Destination city/state")
    equipment_type: Optional[str] = Field(None, description="Type of equipment needed")