from typing import Optional

from pydantic import BaseModel, EmailStr


class AgentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department_id: int


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None