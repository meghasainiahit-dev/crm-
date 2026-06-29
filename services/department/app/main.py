from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="Department")

app.include_router(router)

@app.get("/")
async def home():
    return {
        "message": "Department service is running"
    }
