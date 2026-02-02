from fastapi import FastAPI
from app.database import Base, engine
from app.models import user
from app.models import glucose  # NEW: Import glucose model
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app = FastAPI(title="GlucoTrack API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    """
    Root endpoint - API health check
    """
    return {"message": "GlucoTrack backend is running"}