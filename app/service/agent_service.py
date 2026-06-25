from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.user import User
from app.utils.security import hash_password


def create_agent(db: Session, data, admin):
    department = db.query(Department).filter(
        Department.id == data.department_id,
        Department.company_id == admin.company_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    email_exists = db.query(User).filter(
        User.email == data.email
    ).first()

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    agent = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        role="agent",
        company_id=admin.company_id,
        department_id=department.id,
        created_by=admin.id
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


def get_agents(db: Session, admin):
    return db.query(User).filter(
        User.company_id == admin.company_id,
        User.role == "agent"
    ).all()


def update_agent(
    db: Session,
    agent_id: int,
    data,
    admin
):
    agent = db.query(User).filter(
        User.id == agent_id,
        User.company_id == admin.company_id,
        User.role == "agent"
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "department_id" in update_data:
        department = db.query(Department).filter(
            Department.id == update_data["department_id"],
            Department.company_id == admin.company_id
        ).first()

        if not department:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

    for key, value in update_data.items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    return agent