from datetime import datetime
from uuid import uuid4

from models.static import ContractKeyEnum
from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from utils.database.connection import Base


class Contract(Base):
    __tablename__ = "contracts"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    key = Column(Enum(ContractKeyEnum), nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
