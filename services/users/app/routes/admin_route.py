from fastapi import APIRouter, status

from app.schema.admin_schema import (
    AdminLogin,
    DefaultAdminCreate
)
from app.service.admin_service import (
    create_default_admin,
    login_admin
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/default-admin",
    status_code=status.HTTP_201_CREATED
)
async def create_default_admin_route(
    data: DefaultAdminCreate
):
    return await create_default_admin(data)


@router.post("/login")
async def login_admin_route(
    data: AdminLogin
):
    return await login_admin(data)