from pydantic import BaseModel, Field, field_validator
from datetime import date, time, datetime
from typing import Optional

class GlucoseRecordBase(BaseModel):
    """
    Base schema for glucose record with common fields
    """
    date: date = Field(..., description="Date of the glucose reading")
    time: time = Field(..., description="Time of the glucose reading")
    meal_type: str = Field(..., description="Type of meal: breakfast, lunch, dinner, snack")
    fasting_glucose: Optional[int] = Field(None, ge=0, le=600, description="Fasting glucose level in mg/dL")
    postprandial_glucose: Optional[int] = Field(None, ge=0, le=600, description="Postprandial glucose level in mg/dL")
    insulin_units: Optional[float] = Field(None, ge=0, le=100, description="Insulin units administered")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes about the reading")
    
    @field_validator('meal_type')
    @classmethod
    def validate_meal_type(cls, v: str) -> str:
        """
        Validate that meal_type is one of the allowed values
        """
        allowed_values = ['breakfast', 'lunch', 'dinner', 'snack']
        if v.lower() not in allowed_values:
            raise ValueError(f'meal_type must be one of: {", ".join(allowed_values)}')
        return v.lower()


class GlucoseRecordCreate(GlucoseRecordBase):
    """
    Schema for creating a new glucose record
    
    Inherits all fields from GlucoseRecordBase
    """
    pass


class GlucoseRecordUpdate(BaseModel):
    """
    Schema for updating an existing glucose record
    
    All fields are optional to allow partial updates
    """
    date: Optional[date] = None
    time: Optional[time] = None
    meal_type: Optional[str] = None
    fasting_glucose: Optional[int] = Field(None, ge=0, le=600)
    postprandial_glucose: Optional[int] = Field(None, ge=0, le=600)
    insulin_units: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=500)
    
    @field_validator('meal_type')
    @classmethod
    def validate_meal_type(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate meal_type if provided
        """
        if v is None:
            return v
        allowed_values = ['breakfast', 'lunch', 'dinner', 'snack']
        if v.lower() not in allowed_values:
            raise ValueError(f'meal_type must be one of: {", ".join(allowed_values)}')
        return v.lower()


class GlucoseRecordResponse(GlucoseRecordBase):
    """
    Schema for glucose record response
    
    Includes database fields like id and user_id
    """
    id: int
    user_id: int
    
    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models