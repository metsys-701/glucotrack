from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return {"message": "User created successfully", "user_id": user.id}
