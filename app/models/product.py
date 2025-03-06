from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.product_plan import ProductPlan, ProductPlanBase
from utils.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    plans = relationship(ProductPlan, back_populates="product")


class ProductBase(BaseModel):
    uuid: UUID4
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    plans: list[ProductPlanBase]
