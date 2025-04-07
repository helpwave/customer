from uuid import uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class ProductContract(Base):
    __tablename__ = "product_contracts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("products.uuid"),
        nullable=False,
    )
    contract_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("contracts.uuid"),
        nullable=False,
    )

    contract = relationship("Contract", back_populates="product_contracts")
    product = relationship("Product", back_populates="product_contracts")
