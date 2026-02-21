from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    - Ensures email uniqueness
    - Hashes password securely
    - Stores user in the database
    """

    # Check if email already exists
    existing_user = get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user using CRUD function
    new_user = create_user(db, user_data)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "created_at": new_user.created_at
    }


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT access token.
    Uses OAuth2 password flow (form-data).
    """

    # Retrieve user by email (username field contains email)
    user = get_user_by_email(db, email=form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Generate JWT access token
    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }