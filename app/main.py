from fastapi import FastAPI
from app.database import engine, Base

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.glucose import router as glucose_router


app = FastAPI(title="GlucoTrack API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(glucose_router)

@app.get("/")
def root():
    return {"message": "GlucoTrack backend is running"}