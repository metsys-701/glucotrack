from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class GlucoseRecord(Base):
    """
    Database model for storing blood glucose measurements.
    """

    __tablename__ = "glucose_records"

    id = Column(Integer, primary_key=True, index=True)

    glucose_value = Column(Integer, nullable=False)
    note = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Relationship back to User
    user = relationship(
        "User",
        back_populates="glucose_records"
    )