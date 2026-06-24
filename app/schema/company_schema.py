from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    company_name: str
    address: str
    email: str
    gst: str
    logo: Optional[str] = None
    timezone: str


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    gst: Optional[str] = None
    logo: Optional[str] = None
    timezone: Optional[str] = None