from fastapi import FastAPI
from app.database import Base, engine
from app.models import user
from app.api.routes.auth import router as auth_router  # YENİ SATIR

app = FastAPI(title="GlucoTrack API")

Base.metadata.create_all(bind=engine)

# Router'ı ekle
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])  # YENİ SATIR

@app.get("/")
def root():
    return {"message": "GlucoTrack backend is running"}
