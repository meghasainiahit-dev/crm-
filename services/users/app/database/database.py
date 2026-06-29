import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
DATABASE_NAME=os.getenv("DATABASE_NAME")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env NOT FOUND")
if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME .env NOT FOUND")
client=AsyncMongoClient(DATABASE_URL)
database=client[DATABASE_NAME]

users_collection=database["users"]

async def connect_database():
    await client.admin.command("ping")
    print("mongodb is connected")

async def close_connection():
    await client.close()
    print("mongodb is not connected")