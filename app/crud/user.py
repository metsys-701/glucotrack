from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Yeni kullanıcı oluşturur (MEVCUT - Dokunma)
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
    Email'e göre kullanıcıyı database'den bulur
    
    Args:
        db: Database session
        email: Aranacak email adresi
    
    Returns:
        User object veya None (bulunamazsa)
    
    Kullanım:
        - Register sırasında email kontrolü
        - Login sırasında kullanıcı doğrulama
    """
    return db.query(User).filter(User.email == email).first()