from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserModel(BaseModel):
    id: str | None = Field(
        default=None,
        alias="_id"
    )

    name: str
    email: EmailStr
    hashed_password: str

    role: Literal["admin"] = "admin"

    company_id: str

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    model_config = ConfigDict(
        populate_by_name=True
    )