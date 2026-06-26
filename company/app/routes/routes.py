from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schema.company_schema import (
    CompanyCreate,
    CompanyUpdate
)
from app.service.company_service import (
    create_company,
    get_companies,
    get_company_by_id,
    update_company,
    delete_company
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create(data: CompanyCreate, db: Session = Depends(get_db)):
    return create_company(db, data)


@router.get("/")
def list_company(db: Session = Depends(get_db)):
    return get_companies(db)


@router.put("/{company_id}")
def update(
    company_id: int,
    data: CompanyUpdate,
    db: Session = Depends(get_db)
):
    company = update_company(
        db,
        company_id,
        data
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company

@router.get("/{company_id}")
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    company = get_company_by_id(
        db,
        company_id
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


@router.delete("/{company_id}")
def delete(
    company_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_company(
        db,
        company_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return {
        "message": "Company deleted successfully"
    }