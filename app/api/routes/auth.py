from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.jwt import create_access_token

from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin, Token
from app.crud.user import create_user, get_user_by_email
from app.database import get_db  
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account
    
    Args:
        user_in: User registration data (email, password)
        db: Database session
    
    Returns:
        Success message with user ID
    
    Raises:
        HTTPException: If email is already registered
    """
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return {"message": "User created successfully", "user_id": user.id}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT access token
    
    Args:
        user_data: Login credentials (email, password)
        db: Database session
    
    Returns:
        JWT access token and token type
    
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = get_user_by_email(db, email=user_data.email)
    
    # Return error if user not found
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # Create JWT token with user email as subject
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }