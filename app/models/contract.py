from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from models.product_contract import ProductContract
from models.static import ContractKeyEnum
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class Contract(Base):
    __tablename__ = "contracts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    key = Column(Enum(ContractKeyEnum), nullable=False)
    version = Column(String, nullable=False)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    product_contracts = relationship(
        ProductContract, back_populates="contract"
    )


class ContractBase(BaseModel):
    uuid: UUID4
    key: ContractKeyEnum
    version: str
    url: str | None
    created_at: datetime


class ContractsByProductRead(BaseModel):
    products: list[UUID4]
