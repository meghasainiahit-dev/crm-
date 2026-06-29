from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Companycreate(BaseModel):
    company_name:str
    address:str
    email:EmailStr
    mobile_no:str
    contact_no:str
    gst:str
    logo:str
    landmark:Optional[str]=None
    area:Optional[str]=None
    city:str
    state:str
    country:str
    pincode:str
    ceo_name:Optional[str]=None
    timezone:str

    admin_name: str
    admin_email: EmailStr

    admin_password: str = Field(
        min_length=8
    )




class Companyupdate(BaseModel):
    company_name:Optional[str]=None
    address:Optional[str]=None
    email:Optional[str]=None
    mobile_no:Optional[str]=None
    contact_no:Optional[str]=None
    gst:Optional[str]=None
    logo:Optional[str]=None
    landmark:Optional[str]=None
    area:Optional[str]=None
    city:Optional[str]=None
    state:Optional[str]=None
    country:Optional[str]=None
    pincode:Optional[str]=None
    ceo_name:Optional[str]=None
    timezone:Optional[str]=None

    