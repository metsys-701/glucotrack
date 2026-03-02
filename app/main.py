from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.glucose import router as glucose_router


app = FastAPI(title="GlucoTrack API")

# Enable CORS for frontend (React running on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(glucose_router)


@app.get("/")
def root():
    """
    Root endpoint - API health check
    """
    return {"message": "GlucoTrack backend is running"}