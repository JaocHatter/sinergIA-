from fastapi import FastAPI
from app.api._init__ import router
app = FastAPI()

app = FastAPI(
    title="LabLab Hackathon", 
    description="Multi Agetn System for Knowledge Graph Construction",
    version="0.1"
)

app.include_router(router, prefix="/api")