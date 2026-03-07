from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class GlucoseRecord(Base):

    __tablename__ = "glucose_records"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    glucose_value = Column(Integer, nullable=False)

    measurement_type = Column(String, nullable=False)

    insulin_type = Column(String, nullable=True)

    insulin_units = Column(Integer, default=0)

    note = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())