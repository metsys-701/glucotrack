from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_db
from app.crud.user import get_user_by_email

# OAuth2 scheme for token extraction from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Dictionary containing token payload (e.g., {"sub": "user@example.com"})
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    # Copy the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add expiration to token payload
    to_encode.update({"exp": expire})
    
    # Encode and return JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and validate JWT access token
    
    Args:
        token: JWT token string
    
    Returns:
        Email from token payload (subject) if valid, None otherwise
    
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract email from 'sub' field
        email: str = payload.get("sub")
        
        # Return None if email not found in token
        if email is None:
            return None
            
        return email
        
    except JWTError:
        # Token is invalid or expired
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        token: JWT token from Authorization header
        db: Database session
    
    Returns:
        User object if token is valid
    
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    # Define credentials exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token and extract email
    email = decode_access_token(token)
    
    # If token is invalid or email not found
    if email is None:
        raise credentials_exception
    
    # Get user from database
    user = get_user_by_email(db, email=email)
    
    # If user not found in database
    if user is None:
        raise credentials_exception
    
    return user
