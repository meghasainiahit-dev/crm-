from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException

from app.database.database import department_collection
from app.model.model import DepartmentModel
from app.schema.schema import (
    DepartmentCreate,
    DepartmentUpdate
)


async def create_department(
    data: DepartmentCreate,
    admin: dict
):
    old_department = await department_collection.find_one(
        {
            "department_name": data.department_name,
            "company_id": admin["company_id"]
        }
    )

    if old_department:
        raise HTTPException(
            status_code=409,
            detail="Department already exists"
        )

    department = DepartmentModel(
        department_name=data.department_name,
        description=data.description,
        company_id=admin["company_id"],
        created_by=admin["admin_id"]
    )

    department_data = department.model_dump(
        by_alias=True,
        exclude_none=True
    )

    department_data.pop("_id", None)

    result = await department_collection.insert_one(
        department_data
    )

    department_data["_id"] = str(result.inserted_id)

    return department_data


async def all_get_departments(admin: dict):
    departments = []

    cursor = department_collection.find(
        {
            "company_id": admin["company_id"]
        }
    )

    async for department in cursor:
        department["_id"] = str(department["_id"])
        departments.append(department)

    return departments


async def get_department(
    department_id: str,
    admin: dict
):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid department ID"
        )

    department = await department_collection.find_one(
        {
            "_id": ObjectId(department_id),
            "company_id": admin["company_id"]
        }
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    department["_id"] = str(department["_id"])

    return department


async def update_department(
    department_id: str,
    data: DepartmentUpdate,
    admin: dict
):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid department ID"
        )

    object_id = ObjectId(department_id)

    department = await department_collection.find_one(
        {
            "_id": object_id,
            "company_id": admin["company_id"]
        }
    )

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    update_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No data provided for update"
        )

    if "department_name" in update_data:
        old_department = await department_collection.find_one(
            {
                "_id": {"$ne": object_id},
                "company_id": admin["company_id"],
                "department_name": update_data["department_name"]
            }
        )

        if old_department:
            raise HTTPException(
                status_code=409,
                detail="Department name already exists"
            )

    update_data["updated_at"] = datetime.now(timezone.utc)

    await department_collection.update_one(
        {
            "_id": object_id,
            "company_id": admin["company_id"]
        },
        {
            "$set": update_data
        }
    )

    updated_department = await department_collection.find_one(
        {
            "_id": object_id,
            "company_id": admin["company_id"]
        }
    )

    updated_department["_id"] = str(
        updated_department["_id"]
    )

    return updated_department


async def delete_department(
    department_id: str,
    admin: dict
):
    if not ObjectId.is_valid(department_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid department ID"
        )

    result = await department_collection.delete_one(
        {
            "_id": ObjectId(department_id),
            "company_id": admin["company_id"]
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {
        "message": "Department deleted successfully"
    }