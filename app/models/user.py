from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
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
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    token_version = Column(
        Integer,
        default=1,
        nullable=False
    )