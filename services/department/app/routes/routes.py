from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_admin
from app.schema.schema import (
    DepartmentCreate,
    DepartmentUpdate
)
from app.service.service import (
    all_get_departments,
    create_department,
    delete_department,
    get_department,
    update_department
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def create_department_route(
    data: DepartmentCreate,
    admin: dict = Depends(get_current_admin)
):
    return await create_department(
        data,
        admin
    )


@router.get("/")
async def all_get_departments_route(
    admin: dict = Depends(get_current_admin)
):
    return await all_get_departments(admin)


@router.get("/{department_id}")
async def get_department_route(
    department_id: str,
    admin: dict = Depends(get_current_admin)
):
    return await get_department(
        department_id,
        admin
    )


@router.put("/{department_id}")
async def update_department_route(
    department_id: str,
    data: DepartmentUpdate,
    admin: dict = Depends(get_current_admin)
):
    return await update_department(
        department_id,
        data,
        admin
    )


@router.delete("/{department_id}")
async def delete_department_route(
    department_id: str,
    admin: dict = Depends(get_current_admin)
):
    return await delete_department(
        department_id,
        admin
    )