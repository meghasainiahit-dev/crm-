from pydantic import BaseModel, EmailStr, Field


class DefaultAdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    company_id: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str