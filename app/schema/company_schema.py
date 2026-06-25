from pydantic import BaseModel,EmailStr
from typing import Optional

class CompanyCreate(BaseModel):
    company_name: str
    address: str
    email: str
    gst: str
    logo: Optional[str] = None
    timezone: str
    
    admin_name : str
    admin_email : EmailStr
    admin_password : str

class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    gst: Optional[str] = None
    logo: Optional[str] = None
    timezone: Optional[str] = None

  