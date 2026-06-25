from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(30),
        default="pending",
        nullable=False
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    agent_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    assigned_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )