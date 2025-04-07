from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class CustomerProduct(Base):
    __tablename__ = "customer_products"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_uuid = Column(
        UUID(as_uuid=True), ForeignKey("customers.uuid"), nullable=False
    )
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    product_plan_uuid = Column(
        UUID(as_uuid=True), ForeignKey("product_plans.uuid"), nullable=False
    )
    seats = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    next_payment_date = Column(DateTime, nullable=True)
    voucher_uuid = Column(
        UUID(as_uuid=True), ForeignKey("vouchers.uuid"), nullable=True
    )
    cancellation_date = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer = relationship("Customer", back_populates="products")


class CustomerProductBase(BaseModel):
    uuid: UUID4
    customer_uuid: UUID4
    product_uuid: UUID4
    product_plan_uuid: UUID4
    seats: int | None
    start_date: datetime
    next_payment_date: datetime | None
    voucher_uuid: UUID4 | None
    cancellation_date: datetime | None
    created_at: datetime
    updated_at: datetime


class CustomerProductCreate(BaseModel):
    product_uuid: UUID4
    product_plan_uuid: UUID4
    voucher_uuid: UUID4 | None = None
    accepted_contracts: list[UUID4] = []
