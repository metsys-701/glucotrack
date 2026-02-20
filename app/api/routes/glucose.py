from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.glucose import GlucoseRecord
from app.schemas.glucose import GlucoseCreate, GlucoseResponse
from app.core.jwt import get_current_user
from app.models.user import User

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all glucose records for the authenticated user.
    """

    records = (
        db.query(GlucoseRecord)
        .filter(GlucoseRecord.user_id == current_user.id)
        .all()
    )

    return records


@router.get("/{record_id}", response_model=GlucoseResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single glucose record by ID.
    """

    record = (
        db.query(GlucoseRecord)
        .filter(
            GlucoseRecord.id == record_id,
            GlucoseRecord.user_id == current_user.id
        )
        .first()
    )

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

    record = (
        db.query(GlucoseRecord)
        .filter(
            GlucoseRecord.id == record_id,
            GlucoseRecord.user_id == current_user.id
        )
        .first()
    )

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

    record = (
        db.query(GlucoseRecord)
        .filter(
            GlucoseRecord.id == record_id,
            GlucoseRecord.user_id == current_user.id
        )
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    db.delete(record)
    db.commit()

    return {"message": "Record deleted successfully"}