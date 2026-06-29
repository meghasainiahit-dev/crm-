from datetime import datetime,timezone
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class company_model(BaseModel):
    id:str|None=Field(default=None,alias="_id")
    company_name:str
    address:str
    email:EmailStr
    mobile_no:str
    contact_no:str
    gst:str
    logo:str
    landmark:str|None=None
    area:str|None=None
    city:str
    state:str
    country:str
    pincode:str
    ceo_name:str|None=None
    timezone:str
    is_active:bool=True
    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
)
    updated_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
)    
    model_config=ConfigDict(
        populate_by_name=True
    )

