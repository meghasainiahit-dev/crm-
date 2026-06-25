from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.task import Task
from app.models.user import User


def create_task(db: Session, data, admin):
    department = db.query(Department).filter(
        Department.id == data.department_id,
        Department.company_id == admin.company_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    agent = db.query(User).filter(
        User.id == data.agent_id,
        User.company_id == admin.company_id,
        User.department_id == data.department_id,
        User.role == "agent",
        User.is_active.is_(True)
    ).first()

    if not agent:
        raise HTTPException(
            status_code=400,
            detail="Agent does not belong to this department"
        )

    task = Task(
        title=data.title,
        description=data.description,
        status="pending",
        company_id=admin.company_id,
        department_id=data.department_id,
        agent_id=agent.id,
        assigned_by=admin.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(db: Session, admin):
    return db.query(Task).filter(
        Task.company_id == admin.company_id
    ).all()


def get_agent_tasks(db: Session, agent):
    return db.query(Task).filter(
        Task.agent_id == agent.id,
        Task.company_id == agent.company_id
    ).all()


def update_task_status(
    db: Session,
    task_id: int,
    data,
    agent
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.agent_id == agent.id,
        Task.company_id == agent.company_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.status = data.status

    db.commit()
    db.refresh(task)

    return task