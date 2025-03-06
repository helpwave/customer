from datetime import datetime
from uuid import uuid4

from models.static import InvoiceStatusEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from utils.database.connection import Base


class Invoice(Base):
    __tablename__ = "invoices"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_uuid = Column(
        UUID(as_uuid=True), ForeignKey("customers.uuid"), nullable=False
    )
    status = Column(Enum(InvoiceStatusEnum), nullable=False)
    date = Column(DateTime, nullable=False)
    total_amount = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    customer = relationship("Customer", back_populates="invoices")
