from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./glucotrack.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# YENİ: Database session dependency
def get_db():
    """
    Her API isteği için yeni bir database session oluşturur
    İstek bitince session otomatik kapanır
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()