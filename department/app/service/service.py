# Business Logic
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.department import Department


def create_department(db: Session, data, admin):
    existing_department = db.query(Department).filter(
        Department.company_id == admin.company_id,
        Department.department_name == data.department_name
    ).first()

    if existing_department:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    department = Department(
        department_name=data.department_name,
        company_id=admin.company_id
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


def get_departments(db: Session, admin):
    return db.query(Department).filter(
        Department.company_id == admin.company_id
    ).all()


def update_department(
    db: Session,
    department_id: int,
    data,
    admin
):
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.company_id == admin.company_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    department.department_name = data.department_name

    db.commit()
    db.refresh(department)

    return department


def delete_department(
    db: Session,
    department_id: int,
    admin
):
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.company_id == admin.company_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }