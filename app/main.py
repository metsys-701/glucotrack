from fastapi import FastAPI
from app.database import Base, engine
from app.models import user
from app.models import glucose
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.glucose import router as glucose_router  # NEW

app = FastAPI(title="GlucoTrack API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(glucose_router)

@app.get("/")
def root():
    return {"message": "GlucoTrack backend is running"}