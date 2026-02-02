from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class GlucoseRecord(Base):
    """
    Glucose record model for storing patient blood sugar readings
    
    Stores daily glucose measurements including fasting and postprandial readings,
    insulin dosage, and related information.
    """
    __tablename__ = "glucose_records"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Date and time information
    date = Column(Date, nullable=False, index=True)  # Record date
    time = Column(Time, nullable=False)  # Record time
    
    # Meal type: breakfast, lunch, dinner, snack
    meal_type = Column(String, nullable=False)
    
    # Glucose readings (mg/dL)
    fasting_glucose = Column(Integer, nullable=True)  # Before meal
    postprandial_glucose = Column(Integer, nullable=True)  # 2 hours after meal
    
    # Insulin dosage (units)
    insulin_units = Column(Float, nullable=True)
    
    # Optional notes
    notes = Column(String, nullable=True)
    
    # Relationship to User
    user = relationship("User", back_populates="glucose_records")