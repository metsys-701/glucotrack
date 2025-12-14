from fastapi import FastAPI
from app.database import Base, engine
from app.models import user

app = FastAPI(title="GlucoTrack API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "GlucoTrack backend is running"}
