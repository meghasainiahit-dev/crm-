from fastapi import FastAPI
from sqlalchemy import text

from app.routes.company_route import router as company_router
from app.database.database import engine
from app.models.company import Company

app = FastAPI(
    title="CRM API",
    version="1.0.0"
)

# Create tables
Company.metadata.create_all(bind=engine)

app.include_router(company_router)

@app.get("/")
def home():
    return {"message": "CRM API Running Successfully"}