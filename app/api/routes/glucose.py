from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date as date_type

from app.core.jwt import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.glucose import GlucoseRecordCreate, GlucoseRecordUpdate, GlucoseRecordResponse
from app.crud.glucose import (
    create_glucose_record,
    get_glucose_records,
    get_glucose_record_by_id,
    update_glucose_record,
    delete_glucose_record
)

router = APIRouter()


@router.post("", response_model=GlucoseRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    record: GlucoseRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new glucose record for the authenticated user
    
    Args:
        record: Glucose record data
        current_user: Authenticated user (from JWT token)
        db: Database session
    
    Returns:
        Created glucose record
    """
    db_record = create_glucose_record(db, record, current_user.id)
    return db_record


@router.get("", response_model=List[GlucoseRecordResponse])
async def list_records(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    start_date: Optional[date_type] = Query(None, description="Filter from this date"),
    end_date: Optional[date_type] = Query(None, description="Filter until this date"),
    meal_type: Optional[str] = Query(None, description="Filter by meal type"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get glucose records for the authenticated user with optional filtering
    
    Supports pagination and filtering by date range and meal type
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum records to return
        start_date: Filter records from this date onwards
        end_date: Filter records until this date
        meal_type: Filter by meal type (breakfast, lunch, dinner, snack)
        current_user: Authenticated user
        db: Database session
    
    Returns:
        List of glucose records
    """
    records = get_glucose_records(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        meal_type=meal_type
    )
    return records


@router.get("/{record_id}", response_model=GlucoseRecordResponse)
async def get_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific glucose record by ID
    
    Only returns the record if it belongs to the authenticated user
    
    Args:
        record_id: ID of the glucose record
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Glucose record
    
    Raises:
        HTTPException: 404 if record not found or doesn't belong to user
    """
    db_record = get_glucose_record_by_id(db, record_id, current_user.id)
    
    if not db_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Glucose record not found"
        )
    
    return db_record


@router.put("/{record_id}", response_model=GlucoseRecordResponse)
async def update_record(
    record_id: int,
    record_update: GlucoseRecordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing glucose record
    
    Only updates the record if it belongs to the authenticated user
    Supports partial updates (only provided fields are updated)
    
    Args:
        record_id: ID of the record to update
        record_update: Fields to update
        current_user: Authenticated user
        db: Database session
    
    Returns:
        Updated glucose record
    
    Raises:
        HTTPException: 404 if record not found or doesn't belong to user
    """
    db_record = update_glucose_record(db, record_id, current_user.id, record_update)
    
    if not db_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Glucose record not found"
        )
    
    return db_record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a glucose record
    
    Only deletes the record if it belongs to the authenticated user
    
    Args:
        record_id: ID of the record to delete
        current_user: Authenticated user
        db: Database session
    
    Raises:
        HTTPException: 404 if record not found or doesn't belong to user
    """
    success = delete_glucose_record(db, record_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Glucose record not found"
        )
    
    # 204 No Content - no response body
    return None