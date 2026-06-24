from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255))
    address = Column(String(500))
    email = Column(String(255))
    gst = Column(String(100))
    logo = Column(String(255))
    timezone = Column(String(100))