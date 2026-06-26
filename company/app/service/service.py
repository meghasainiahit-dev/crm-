from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User
from app.utils.security import hash_password


def create_company(db: Session, data):
    company_exists = db.query(Company).filter(
        Company.email == data.email
    ).first()

    if company_exists:
        raise HTTPException(
            status_code=400,
            detail="Company email already registered"
        )

    admin_exists = db.query(User).filter(
        User.email == data.admin_email
    ).first()

    if admin_exists:
        raise HTTPException(
            status_code=400,
            detail="Admin email already registered"
        )

    company = Company(
        company_name=data.company_name,
        address=data.address,
        email=data.email,
        mobile_number=data.mobile_number,
        contact_person=data.contact_person,
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

    try:
        db.add(company)

        # Company ki ID commit se pehle mil jaayegi
        db.flush()

        admin = User(
            name=data.admin_name,
            email=data.admin_email,
            hashed_password=hash_password(data.admin_password),
            role="admin",
            company_id=company.id,
            department_id=None,
            created_by=None,
            is_active=True
        )

        db.add(admin)
        db.commit()

        db.refresh(company)
        db.refresh(admin)

        return {
            "message": "Company and default admin created successfully",
            "company": {
                "id": company.id,
                "company_name": company.company_name,
                "address": company.address,
                "email": company.email,
                "mobile_number": company.mobile_number,
                "contact_person": company.contact_person,
                "gst": company.gst,
                "logo": company.logo,
                "landmark": company.landmark,
                "area": company.area,
                "city": company.city,
                "state": company.state,
                "country": company.country,
                "pincode": company.pincode,
                "ceo_name": company.ceo_name,
                "timezone": company.timezone
            },
            "admin": {
                "id": admin.id,
                "name": admin.name,
                "email": admin.email,
                "role": admin.role
            }
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Company or admin data already exists"
        )

    except Exception:
        db.rollback()
        raise


def get_companies(db: Session):
    return db.query(Company).all()


def get_company_by_id(db: Session, company_id: int):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company


def update_company(
    db: Session,
    company_id: int,
    data
):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    if "email" in update_data:
        email_exists = db.query(Company).filter(
            Company.email == update_data["email"],
            Company.id != company_id
        ).first()

        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="Company email already registered"
            )

    for field, value in update_data.items():
        setattr(company, field, value)

    try:
        db.commit()
        db.refresh(company)

        return company

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Unable to update company"
        )

    except Exception:
        db.rollback()
        raise


def delete_company(
    db: Session,
    company_id: int
):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    try:
        db.delete(company)
        db.commit()

        return {
            "message": "Company deleted successfully"
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Company cannot be deleted because related data exists"
        )

    except Exception:
        db.rollback()
        raise