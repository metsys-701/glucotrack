from fastapi import APIRouter, Depends
from app.core.jwt import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    
    Args:
        current_user: Automatically injected authenticated user
    
    Returns:
        User information (id, email, created_at)
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "created_at": current_user.created_at
    }