from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    department_name: str


class DepartmentUpdate(BaseModel):
    department_name: str