from datetime import datetime
from pydantic import BaseModel


class GlucoseBase(BaseModel):
    glucose_value: int
    note: str | None = None


class GlucoseCreate(GlucoseBase):
    """
    Schema for creating a glucose record.
    """
    pass


class GlucoseResponse(GlucoseBase):
    """
    Schema for returning glucose record data.
    """

    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True