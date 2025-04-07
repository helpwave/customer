from datetime import datetime
from uuid import uuid4

from models.static import RoleEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_uuid = Column(
        UUID(as_uuid=True), ForeignKey("customers.uuid"), nullable=True
    )
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.NORMAL)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer = relationship("Customer", back_populates="users")
