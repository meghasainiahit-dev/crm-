from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="Agent")

app.include_router(router)
