from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user in the database
    
    Args:
        db: Database session
        user_in: User data (email, password)
    
    Returns:
        Created User object with generated ID
    """
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    """
    Retrieve user by email address
    
    Args:
        db: Database session
        email: Email address to search for
    
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()