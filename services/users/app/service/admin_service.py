from fastapi import HTTPException

from app.database.database import users_collection
from app.model.admin_model import UserModel
from app.schema.admin_schema import (
    AdminLogin,
    DefaultAdminCreate
)
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password
)


async def create_default_admin(data: DefaultAdminCreate):

    old_admin = await users_collection.find_one(
        {"email": data.email}
    )

    if old_admin:
        raise HTTPException(
            status_code=409,
            detail="Admin email already exists"
        )

    admin = UserModel(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        company_id=data.company_id
    )

    admin_data = admin.model_dump(
        by_alias=True,
        exclude_none=True
    )

    admin_data.pop("_id", None)

    result = await users_collection.insert_one(
        admin_data
    )

    return {
        "_id": str(result.inserted_id),
        "name": admin_data["name"],
        "email": admin_data["email"],
        "role": admin_data["role"],
        "company_id": admin_data["company_id"]
    }


async def login_admin(data: AdminLogin):

    admin = await users_collection.find_one(
        {"email": data.email}
    )

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = verify_password(
        data.password,
        admin["hashed_password"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": str(admin["_id"]),
            "company_id": admin["company_id"],
            "role": admin["role"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }