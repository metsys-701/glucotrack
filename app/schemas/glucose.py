from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GlucoseCreate(BaseModel):

    glucose_value: int

    measurement_type: str

    note: Optional[str] = None


class GlucoseResponse(BaseModel):

    id: int

    user_id: int

    glucose_value: int

    measurement_type: str

    note: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True