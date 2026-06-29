from fastapi import FastAPI
from app.routes.admin_route import router

app = FastAPI(title="Agent")

app.include_router(router)

@app.get("/")
async def home():
    return {
        "message": "User service is running"
    }