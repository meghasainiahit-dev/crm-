from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from app.database.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    department_name = Column(
        String(150),
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "department_name",
            name="unique_company_department"
        ),
    )