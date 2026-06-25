from fastapi import FastAPI
from sqlalchemy import text

from app.routes.company_route import router as company_router
from app.database.database import engine
from app.models.company import Company
from app.models import department, task, user
from app.routes import (
    agent_route,
    auth_route,
    company_route,
    department_route,
    task_route
)


app = FastAPI(
    title="CRM API",
    version="1.0.0"
)

# Create tables
Company.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(company_route.router)
app.include_router(auth_route.router)
app.include_router(department_route.router)
app.include_router(agent_route.router)
app.include_router(task_route.router)

@app.get("/")
def home():
    return {"message": "CRM API Running Successfully"}