from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from app.models.glucose import GlucoseRecord
from app.schemas.glucose import GlucoseRecordCreate, GlucoseRecordUpdate
from typing import List, Optional
from datetime import date

def create_glucose_record(db: Session, record: GlucoseRecordCreate, user_id: int) -> GlucoseRecord:
    """
    Create a new glucose record for a specific user
    
    Args:
        db: Database session
        record: Glucose record data from request
        user_id: ID of the authenticated user
    
    Returns:
        Created GlucoseRecord object
    """
    db_record = GlucoseRecord(
        user_id=user_id,
        date=record.date,
        time=record.time,
        meal_type=record.meal_type,
        fasting_glucose=record.fasting_glucose,
        postprandial_glucose=record.postprandial_glucose,
        insulin_units=record.insulin_units,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_glucose_records(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    meal_type: Optional[str] = None
) -> List[GlucoseRecord]:
    """
    Get glucose records for a specific user with optional filtering
    
    Args:
        db: Database session
        user_id: ID of the user
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        start_date: Filter records from this date onwards
        end_date: Filter records until this date
        meal_type: Filter by meal type (breakfast, lunch, dinner, snack)
    
    Returns:
        List of GlucoseRecord objects
    """
    query = db.query(GlucoseRecord).filter(GlucoseRecord.user_id == user_id)
    
    # Apply date filters if provided
    if start_date:
        query = query.filter(GlucoseRecord.date >= start_date)
    if end_date:
        query = query.filter(GlucoseRecord.date <= end_date)
    
    # Apply meal type filter if provided
    if meal_type:
        query = query.filter(GlucoseRecord.meal_type == meal_type.lower())
    
    # Order by date and time (newest first)
    query = query.order_by(desc(GlucoseRecord.date), desc(GlucoseRecord.time))
    
    # Apply pagination
    return query.offset(skip).limit(limit).all()


def get_glucose_record_by_id(db: Session, record_id: int, user_id: int) -> Optional[GlucoseRecord]:
    """
    Get a specific glucose record by ID
    
    Ensures the record belongs to the authenticated user
    
    Args:
        db: Database session
        record_id: ID of the glucose record
        user_id: ID of the authenticated user
    
    Returns:
        GlucoseRecord object if found and belongs to user, None otherwise
    """
    return db.query(GlucoseRecord).filter(
        and_(
            GlucoseRecord.id == record_id,
            GlucoseRecord.user_id == user_id
        )
    ).first()


def update_glucose_record(
    db: Session,
    record_id: int,
    user_id: int,
    record_update: GlucoseRecordUpdate
) -> Optional[GlucoseRecord]:
    """
    Update an existing glucose record
    
    Args:
        db: Database session
        record_id: ID of the record to update
        user_id: ID of the authenticated user
        record_update: Updated data
    
    Returns:
        Updated GlucoseRecord object if found and updated, None otherwise
    """
    # Get the record (ensures it belongs to user)
    db_record = get_glucose_record_by_id(db, record_id, user_id)
    
    if not db_record:
        return None
    
    # Update only provided fields
    update_data = record_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_glucose_record(db: Session, record_id: int, user_id: int) -> bool:
    """
    Delete a glucose record
    
    Args:
        db: Database session
        record_id: ID of the record to delete
        user_id: ID of the authenticated user
    
    Returns:
        True if deleted successfully, False if record not found
    """
    db_record = get_glucose_record_by_id(db, record_id, user_id)
    
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True