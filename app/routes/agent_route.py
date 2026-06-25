from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schema.agent_schema import AgentCreate, AgentUpdate
from app.service.agent_service import (
    create_agent,
    get_agents,
    update_agent
)
from app.utils.dependencies import require_admin


router = APIRouter(
    prefix="/agents",
    tags=["Agents"]
)


@router.post("/")
def create(
    data: AgentCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return create_agent(db, data, admin)


@router.get("/")
def list_agents(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return get_agents(db, admin)


@router.put("/{agent_id}")
def update(
    agent_id: int,
    data: AgentUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    return update_agent(
        db,
        agent_id,
        data,
        admin
    )