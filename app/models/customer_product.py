from datetime import datetime
from uuid import uuid4

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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    customer = relationship("Customer", back_populates="products")
