from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from models.static import PlanTypeEnum
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class ProductPlan(Base):
    __tablename__ = "product_plans"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    type = Column(Enum(PlanTypeEnum), nullable=False)
    cost_euro = Column(Numeric, nullable=False)
    seat_based = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    product = relationship("Product", back_populates="plans")


class ProductPlanBase(BaseModel):
    uuid: UUID4
    type: PlanTypeEnum
    cost_euro: float
    seat_based: bool
    created_at: datetime
    updated_at: datetime
