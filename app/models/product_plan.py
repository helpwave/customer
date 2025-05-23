from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.static import PlanTypeEnum
from utils.database.connection import Base


class ProductPlan(Base):
    __tablename__ = "product_plans"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    type = Column(Enum(PlanTypeEnum), nullable=False)
    name = Column(String, nullable=False)
    cost_euro = Column(Numeric, nullable=False)
    recurring_month = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    product = relationship("Product", back_populates="plans")
    customer_products = relationship(
        "CustomerProduct",
        back_populates="product_plan")

    vouchers = relationship(
        "Voucher",
        back_populates="product_plan")


class ProductPlanBase(BaseModel):
    uuid: UUID4
    type: PlanTypeEnum
    name: str
    cost_euro: float
    recurring_month: int
    created_at: datetime
    updated_at: datetime
