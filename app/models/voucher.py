from datetime import datetime
from uuid import UUID as UUID4
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from utils.database.connection import Base


class Voucher(Base):
    __tablename__ = "vouchers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, unique=True, nullable=False)
    description = Column(Text)
    product_plan_uuid = Column(
        UUID(as_uuid=True), ForeignKey("product_plans.uuid"), nullable=True
    )
    discount_percentage = Column(Numeric, nullable=True)
    discount_fixed_amount = Column(Numeric, nullable=True)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    max_redemptions = Column(Integer, nullable=False)
    redeemed_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def valid(self) -> bool:
        now = datetime.now()
        time_validity = bool(self.valid_from <= now <= self.valid_until)

        redemption_validity = bool(self.redeemed_count <= self.max_redemptions)

        return time_validity and redemption_validity


class VoucherBase(BaseModel):
    uuid: UUID4
    description: str
    product_plan_uuid: UUID4
    discount_percentage: float
    discount_fixed_amount: float
    valid: bool
