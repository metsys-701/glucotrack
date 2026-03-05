from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.glucose import GlucoseRecord
from app.models.user import User
from app.schemas.glucose import GlucoseCreate, GlucoseResponse
from app.core.jwt import get_current_user


router = APIRouter()


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


@router.get("/")
def list_records(
    skip: int = 0,
    limit: int = 10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve paginated glucose records for the authenticated user.
    Supports pagination and optional date filtering.
    """

    query = db.query(GlucoseRecord).filter(
        GlucoseRecord.user_id == current_user.id
    )

    # Apply start date filter
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(GlucoseRecord.created_at >= start)

    # Apply end date filter
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(GlucoseRecord.created_at <= end)

    total = query.count()

    records = (
        query.order_by(GlucoseRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": records
    }


@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a glucose record belonging to the authenticated user.
    """

    record = db.query(GlucoseRecord).filter(
        GlucoseRecord.id == record_id,
        GlucoseRecord.user_id == current_user.id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted"}


@router.get("/dashboard")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Return dashboard statistics for glucose data.
    Includes averages and time-in-range metrics.
    """

    records = db.query(GlucoseRecord).filter(
        GlucoseRecord.user_id == current_user.id
    ).order_by(GlucoseRecord.created_at.asc()).all()

    if not records:
        return {
            "today_avg": None,
            "last_measurement": None,
            "time_in_range": 0,
            "tight_range": 0,
            "weekly_avg": None
        }

    values = [r.glucose_value for r in records]

    # Last measurement
    last_measurement = records[-1].glucose_value

    # Time in range (70-180 mg/dL)
    tir = len([v for v in values if 70 <= v <= 180]) / len(values) * 100

    # Tight control range (70-140 mg/dL)
    tight = len([v for v in values if 70 <= v <= 140]) / len(values) * 100

    # Weekly average
    week_ago = datetime.utcnow() - timedelta(days=7)

    weekly_records = [
        r.glucose_value for r in records
        if r.created_at >= week_ago
    ]

    weekly_avg = (
        sum(weekly_records) / len(weekly_records)
        if weekly_records else None
    )

    # Today's average
    today = datetime.utcnow().date()

    today_records = [
        r.glucose_value for r in records
        if r.created_at.date() == today
    ]

    today_avg = (
        sum(today_records) / len(today_records)
        if today_records else None
    )

    return {
        "today_avg": round(today_avg, 1) if today_avg else None,
        "last_measurement": last_measurement,
        "time_in_range": round(tir, 1),
        "tight_range": round(tight, 1),
        "weekly_avg": round(weekly_avg, 1) if weekly_avg else None
    }