from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.static import InvoiceStatusEnum
from utils.database.connection import Base


class Invoice(Base):
    __tablename__ = "invoices"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_uuid = Column(
        UUID(as_uuid=True), ForeignKey("customers.uuid"), nullable=False
    )
    status = Column(
        Enum(InvoiceStatusEnum),
        nullable=False,
        default=InvoiceStatusEnum.PENDING,
    )
    date = Column(DateTime, nullable=False)
    total_amount = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    customer = relationship("Customer", back_populates="invoices")


class InvoiceBase(BaseModel):
    uuid: UUID4
    status: InvoiceStatusEnum
    date: datetime
    total_amount: float
    created_at: datetime
    updated_at: datetime
