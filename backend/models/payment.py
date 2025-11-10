from sqlalchemy import Column, BigInteger, String, Numeric, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    due_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    status = Column(String(20), nullable=False, default="Unpaid", index=True)
    payment_method = Column(String(50))
    transaction_id = Column(String(255))
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('Paid', 'Due', 'Unpaid', 'Partial')", name="chk_payment_status"),
    )

