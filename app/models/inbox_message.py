from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.static import MessageStatusEnum
from utils.database.connection import Base


class InboxMessage(Base):
    __tablename__ = "inbox_messages"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_uuid = Column(
        UUID(as_uuid=True), ForeignKey("customers.uuid"), nullable=False
    )
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(Enum(MessageStatusEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    customer = relationship("Customer", back_populates="inbox_messages")
