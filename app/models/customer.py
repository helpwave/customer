from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from utils.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    website_url = Column(String)
    address = Column(String)
    house_number = Column(String)
    care_of = Column(String)
    postal_code = Column(String)
    city = Column(String)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    users = relationship("User", back_populates="customer")
    products = relationship("CustomerProduct", back_populates="customer")
    invoices = relationship("Invoice", back_populates="customer")
    inbox_messages = relationship("InboxMessage", back_populates="customer")
