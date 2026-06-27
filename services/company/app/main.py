from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="Company")

app.include_router(router)
