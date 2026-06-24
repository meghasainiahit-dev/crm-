from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine


app = FastAPI()


