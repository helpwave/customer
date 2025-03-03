from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Numeric
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
    cost_euro = Column(Numeric, nullable=False)
    seat_based = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    product = relationship("Product", back_populates="plans")
