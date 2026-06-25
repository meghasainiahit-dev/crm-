from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schema.department_schema import (
    DepartmentCreate,
    DepartmentUpdate
)
from app.service.department_service import (
    create_department,
    delete_department,
    get_departments,
    update_department
)
from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/")
def create(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return create_department(db, data, admin)


@router.get("/")
def list_departments(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_departments(db, admin)


@router.put("/{department_id}")
def update(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return update_department(
        db,
        department_id,
        data,
        admin
    )


@router.delete("/{department_id}")
def delete(
    department_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return delete_department(
        db,
        department_id,
        admin
    )