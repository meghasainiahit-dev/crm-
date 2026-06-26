
from pydantic import BaseModel,EmailStr

from typing import Optional


class CompanyCreate(BaseModel):
    company_name: str
    address: str
    email: EmailStr
    mobile_number: str
    contact_person: str
    gst: str
    logo: Optional[str] = None
    landmark: Optional[str] = None
    area: Optional[str] = None
    city: str
    state: str
    country: str
    pincode: str
    ceo_name: Optional[str] = None
    timezone: str
    
    admin_name : str
    admin_email : EmailStr
    admin_password : str

class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    contact_person: Optional[str] = None
    gst: Optional[str] = None
    logo: Optional[str] = None
    timezone: Optional[str] = None
    landmark: Optional[str] = None
    area: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    ceo_name: Optional[str] = None
    timezone: Optional[str] = None
