from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from models.product_contract import ProductContract
from models.product_plan import ProductPlan, ProductPlanBase
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    plans = relationship(ProductPlan, back_populates="product")
    product_contracts = relationship(ProductContract, back_populates="product")
    customer_products = relationship(
        "CustomerProduct", back_populates="product")


class ProductBase(BaseModel):
    uuid: UUID4
    name: str
    description: str | None
    image_url: str | None
    created_at: datetime
    updated_at: datetime
    plans: list[ProductPlanBase]
