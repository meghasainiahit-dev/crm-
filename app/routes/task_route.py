from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schema.task_schema import TaskCreate, TaskStatusUpdate
from app.service.task_service import (
    create_task,
    get_agent_tasks,
    get_all_tasks,
    update_task_status
)
from app.utils.dependencies import require_admin, require_agent


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/")
def create(
    data: TaskCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return create_task(db, data, admin)


@router.get("/")
def list_all_tasks(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_all_tasks(db, admin)


@router.get("/my")
def my_tasks(
    db: Session = Depends(get_db),
    agent: User = Depends(require_agent)
):
    return get_agent_tasks(db, agent)


@router.patch("/{task_id}/status")
def change_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    agent: User = Depends(require_agent)
):
    return update_task_status(
        db,
        task_id,
        data,
        agent
    )