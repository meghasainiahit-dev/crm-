from typing import Literal, Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    department_id: int
    agent_id: int


class TaskStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "in_progress",
        "completed",
        "cancelled"
    ]