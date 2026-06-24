from sqlalchemy.orm import Session
from app.models.company import Company


def create_company(db: Session, data):
    company = Company(**data.dict())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_companies(db: Session):
    return db.query(Company).all()


def update_company(db: Session, company_id: int, data):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        return None

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


def delete_company(db: Session, company_id: int):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        return False

    db.delete(company)
    db.commit()

    return True