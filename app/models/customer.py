from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.customer_product import CustomerProduct
from models.invoice import Invoice
from models.message import Message
from models.user import User
from utils.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    website_url = Column(String)
    address = Column(String, nullable=False)
    house_number = Column(String, nullable=False)
    care_of = Column(String)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    users = relationship(User, back_populates="customer")
    products = relationship(CustomerProduct, back_populates="customer")
    invoices = relationship(Invoice, back_populates="customer")
    messages = relationship(Message, back_populates="customer")


class CustomerBase(BaseModel):
    uuid: UUID4
    name: str
    email: str
    website_url: str | None
    address: str | None
    house_number: str | None
    care_of: str | None
    postal_code: str | None
    city: str | None
    country: str | None
    created_at: datetime
    updated_at: datetime


class CustomerCreate(BaseModel):
    name: str
    email: str
    website_url: str | None
    address: str | None
    house_number: str | None
    care_of: str | None
    postal_code: str | None
    city: str | None
    country: str | None


class CustomerRead(BaseModel):
    uuid: UUID4


class CustomerUpdate(BaseModel):
    name: str | None
    email: str | None
    website_url: str | None
    address: str | None
    house_number: str | None
    care_of: str | None
    postal_code: str | None
    city: str | None
    country: str | None


class CustomerDelete(BaseModel):
    uuid: UUID4
