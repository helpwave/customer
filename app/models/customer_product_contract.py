from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from utils.database.connection import Base


class CustomerProductContract(Base):
    __tablename__ = "customer_product_contracts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # TODO reconsider this naming and make it consistent with others
    product_customer_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("customer_products.uuid"),
        nullable=False,
    )
    contract_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("contracts.uuid"),
        nullable=False,
    )
    accepted_at = Column(DateTime, default=datetime.now, nullable=False)
