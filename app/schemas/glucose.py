from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type, time as time_type
from typing import Optional

class GlucoseRecordBase(BaseModel):
    """
    Base schema for glucose record with common fields
    """
    date: date_type = Field(..., description="Date of the glucose reading")
    time: time_type = Field(..., description="Time of the glucose reading")
    meal_type: str = Field(..., description="Type of meal: breakfast, lunch, dinner, snack")
    fasting_glucose: Optional[int] = Field(None, ge=0, le=600, description="Fasting glucose level in mg/dL")
    postprandial_glucose: Optional[int] = Field(None, ge=0, le=600, description="Postprandial glucose level in mg/dL")
    insulin_units: Optional[float] = Field(None, ge=0, le=100, description="Insulin units administered")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes about the reading")
    
    @field_validator('meal_type', mode='before')
    @classmethod
    def validate_meal_type(cls, v):
        """
        Validate that meal_type is one of the allowed values
        """
        if v is None:
            return v
        allowed_values = ['breakfast', 'lunch', 'dinner', 'snack']
        v_lower = str(v).lower()
        if v_lower not in allowed_values:
            raise ValueError(f'meal_type must be one of: {", ".join(allowed_values)}')
        return v_lower


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
    date: Optional[date_type] = None
    time: Optional[time_type] = None
    meal_type: Optional[str] = None
    fasting_glucose: Optional[int] = Field(None, ge=0, le=600)
    postprandial_glucose: Optional[int] = Field(None, ge=0, le=600)
    insulin_units: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=500)
    
    @field_validator('meal_type', mode='before')
    @classmethod
    def validate_meal_type(cls, v):
        """
        Validate meal_type if provided
        """
        if v is None:
            return v
        allowed_values = ['breakfast', 'lunch', 'dinner', 'snack']
        v_lower = str(v).lower()
        if v_lower not in allowed_values:
            raise ValueError(f'meal_type must be one of: {", ".join(allowed_values)}')
        return v_lower


class GlucoseRecordResponse(GlucoseRecordBase):
    """
    Schema for glucose record response
    
    Includes database fields like id and user_id
    """
    id: int
    user_id: int
    
    model_config = {"from_attributes": True}