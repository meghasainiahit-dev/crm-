from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    department_name: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = None


class DepartmentUpdate(BaseModel):
    department_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: str | None = None
    is_active: bool | None = None