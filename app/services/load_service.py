import os
from typing import Dict, Optional, List
import pandas as pd
from fastapi import HTTPException
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class LoadInfo(BaseModel):
    reference_number: str
    origin: str
    destination: str
    equipment_type: str
    rate: float
    commodity: str

class LoadService:
    def __init__(self):
        self.df = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Load and validate CSV data"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'loads.csv')
            
            if not os.path.exists(csv_path):
                logger.error(f"CSV file not found at: {csv_path}")
                raise HTTPException(status_code=500, detail="Load data not available")
                
            # Read CSV with proper data types
            self.df = pd.read_csv(csv_path, dtype={
                'reference_number': str,
                'origin': str,
                'destination': str,
                'equipment_type': str,
                'rate': float,
                'commodity': str
            })
            
            # Validate required columns
            required_columns = ['reference_number', 'origin', 'destination', 
                              'equipment_type', 'rate', 'commodity']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                raise HTTPException(status_code=500, detail="Invalid load data format")
                
            logger.info(f"Successfully loaded {len(self.df)} loads")
            
        except pd.errors.EmptyDataError:
            logger.error("Empty CSV file")
            raise HTTPException(status_code=500, detail="No load data available")
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            raise HTTPException(status_code=500, detail="Error loading load data")

    async def get_load(self, reference_number: str) -> Dict:
        """Get load details by reference number"""
        try:
            if self.df is None:
                self._load_data()
                
            # Clean reference number format
            reference_number = reference_number.upper().strip().replace(" ", "")
            
            # Find matching load
            load = self.df[self.df['reference_number'] == reference_number]
            
            if load.empty:
                logger.warning(f"Load not found: {reference_number}")
                raise HTTPException(status_code=404, detail="Load not found")
                
            # Convert to LoadInfo model and back to dict for validation
            load_info = LoadInfo(**load.iloc[0].to_dict())
            return load_info.dict()
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving load {reference_number}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving load")

    async def search_loads(self, origin: Optional[str] = None, 
                         destination: Optional[str] = None,
                         equipment_type: Optional[str] = None) -> List[Dict]:
        """Search loads based on criteria"""
        try:
            if self.df is None:
                self._load_data()
                
            query = self.df.copy()
            
            if origin:
                query = query[query['origin'].str.contains(origin, case=False, na=False)]
            if destination:
                query = query[query['destination'].str.contains(destination, case=False, na=False)]
            if equipment_type:
                query = query[query['equipment_type'].str.contains(equipment_type, case=False, na=False)]
                
            # Convert results to LoadInfo models for validation
            loads = [LoadInfo(**row).dict() for _, row in query.iterrows()]
            return loads
            
        except Exception as e:
            logger.error(f"Error searching loads: {str(e)}")
            raise HTTPException(status_code=500, detail="Error searching loads")