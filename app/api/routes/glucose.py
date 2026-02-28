from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.glucose import GlucoseRecord
from app.schemas.glucose import GlucoseCreate, GlucoseResponse
from app.models.user import User
from app.core.jwt import get_current_user


router = APIRouter(
    prefix="/glucose",
    tags=["Glucose Records"]
)


@router.post("/", response_model=GlucoseResponse)
def create_record(
    record: GlucoseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new glucose record for the authenticated user.
    """

    new_record = GlucoseRecord(
        glucose_value=record.glucose_value,
        note=record.note,
        user_id=current_user.id
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/", response_model=list[GlucoseResponse])
def list_records(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve glucose records for the authenticated user.
    Optional date filtering supported.
    """

    query = db.query(GlucoseRecord).filter(
        GlucoseRecord.user_id == current_user.id
    )

    if start_date:
        start_date_parsed = datetime.fromisoformat(start_date)
        query = query.filter(GlucoseRecord.created_at >= start_date_parsed)

    if end_date:
        end_date_parsed = datetime.fromisoformat(end_date)
        query = query.filter(GlucoseRecord.created_at <= end_date_parsed)

    return query.all()


@router.get("/{record_id}", response_model=GlucoseResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific glucose record by ID.
    """

    record = db.query(GlucoseRecord).filter(
        GlucoseRecord.id == record_id,
        GlucoseRecord.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    return record


@router.put("/{record_id}", response_model=GlucoseResponse)
def update_record(
    record_id: int,
    updated_data: GlucoseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a glucose record.
    """

    record = db.query(GlucoseRecord).filter(
        GlucoseRecord.id == record_id,
        GlucoseRecord.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    record.glucose_value = updated_data.glucose_value
    record.note = updated_data.note

    db.commit()
    db.refresh(record)

    return record


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a glucose record.
    """

    record = db.query(GlucoseRecord).filter(
        GlucoseRecord.id == record_id,
        GlucoseRecord.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}


@router.get("/stats")
def get_glucose_statistics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Return statistical summary of glucose records for the authenticated user.
    """

    query = db.query(GlucoseRecord).filter(
        GlucoseRecord.user_id == current_user.id
    )

    if start_date:
        start_date_parsed = datetime.fromisoformat(start_date)
        query = query.filter(GlucoseRecord.created_at >= start_date_parsed)

    if end_date:
        end_date_parsed = datetime.fromisoformat(end_date)
        query = query.filter(GlucoseRecord.created_at <= end_date_parsed)

    stats = query.with_entities(
        func.count(GlucoseRecord.id),
        func.avg(GlucoseRecord.glucose_value),
        func.min(GlucoseRecord.glucose_value),
        func.max(GlucoseRecord.glucose_value)
    ).first()

    total_records = stats[0] or 0
    average = float(stats[1]) if stats[1] else 0
    minimum = stats[2] or 0
    maximum = stats[3] or 0

    return {
        "total_records": total_records,
        "average": round(average, 2),
        "min": minimum,
        "max": maximum
    }