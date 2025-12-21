from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin, Token
from app.crud.user import create_user, get_user_by_email
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password

router = APIRouter()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Yeni kullanıcı kaydı oluşturur (MEVCUT - Dokunma)
    """
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(db, user_in)
    return {"message": "User created successfully", "user_id": user.id}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Kullanıcı girişi yapar
    
    Adımlar:
    1. Email'e göre kullanıcıyı bul
    2. Kullanıcı yoksa hata döndür
    3. Şifreyi doğrula
    4. Şifre yanlışsa hata döndür
    5. Her şey tamam ise token döndür (şimdilik dummy)
    """
    # 1. Kullanıcıyı email'e göre bul
    user = get_user_by_email(db, email=user_data.email)
    
    # 2. Kullanıcı yoksa hata
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # 3. Şifreyi doğrula
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email veya şifre hatalı"
        )
    
    # 4. Her şey tamam, token döndür (şimdilik dummy token)
    # İleride JWT token üretimi ekleyeceğiz
    return {
        "access_token": f"dummy_token_for_{user.email}",
        "token_type": "bearer"
    }