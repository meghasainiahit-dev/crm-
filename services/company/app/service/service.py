import os
from datetime import datetime, timezone

import httpx
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import HTTPException

from app.database.database import company_collection
from app.model.model import company_model
from app.schema.schema import Companycreate, Companyupdate


load_dotenv()

USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://127.0.0.1:8003"
)


async def create_company(data: Companycreate):

    old_company = await company_collection.find_one(
        {"email": data.email}
    )

    if old_company:
        raise HTTPException(
            status_code=409,
            detail="Company already exists"
        )

    company = company_model(
        company_name=data.company_name,
        address=data.address,
        email=data.email,
        mobile_no=data.mobile_no,
        contact_no=data.contact_no,
        gst=data.gst,
        logo=data.logo,
        landmark=data.landmark,
        area=data.area,
        city=data.city,
        state=data.state,
        country=data.country,
        pincode=data.pincode,
        ceo_name=data.ceo_name,
        timezone=data.timezone
    )

    company_data = company.model_dump(
        by_alias=True,
        exclude_none=True
    )

    company_data.pop("_id", None)

    result = await company_collection.insert_one(
        company_data
    )

    company_id = str(result.inserted_id)

    admin_data = {
        "name": data.admin_name,
        "email": data.admin_email,
        "password": data.admin_password,
        "company_id": company_id
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USER_SERVICE_URL}/users/default-admin",
                json=admin_data,
                timeout=10
            )

    except httpx.RequestError:
        await company_collection.delete_one(
            {"_id": result.inserted_id}
        )

        raise HTTPException(
            status_code=503,
            detail="User service is not available"
        )

    if response.status_code != 201:
        await company_collection.delete_one(
            {"_id": result.inserted_id}
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get(
                "detail",
                "Admin could not be created"
            )
        )

    company_data["_id"] = company_id

    return {
        "company": company_data,
        "admin": response.json()
    }


async def all_get_companies():

    companies = []

    cursor = company_collection.find()

    async for company in cursor:
        company["_id"] = str(company["_id"])
        companies.append(company)

    return companies



async def get_company(company_id: str):

    if not ObjectId.is_valid(company_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid company ID"
        )

    company = await company_collection.find_one(
        {"_id": ObjectId(company_id)}
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    company["_id"] = str(company["_id"])

    return company



async def update_company(
    company_id: str,
    data: Companyupdate
):

    if not ObjectId.is_valid(company_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid company ID"
        )

    object_id = ObjectId(company_id)

    company = await company_collection.find_one(
        {"_id": object_id}
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    update_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    update_data["updated_at"] = datetime.now(
        timezone.utc
    )

    await company_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    updated_company = await company_collection.find_one(
        {"_id": object_id}
    )

    updated_company["_id"] = str(
        updated_company["_id"]
    )

    return updated_company



async def delete_company(company_id: str):

    if not ObjectId.is_valid(company_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid company ID"
        )

    result = await company_collection.delete_one(
        {"_id": ObjectId(company_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {
        "message": "Company deleted successfully"
    }