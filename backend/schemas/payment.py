from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PaymentCreate(BaseModel):
    order_id: int
    due_amount: Decimal = Decimal("0.00")
    amount: Decimal = Decimal("0.00")
    status: str = "Unpaid"
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentUpdate(BaseModel):
    due_amount: Optional[Decimal] = None
    amount: Optional[Decimal] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    paid_at: Optional[datetime] = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    due_amount: Decimal
    amount: Decimal
    status: str
    payment_method: Optional[str]
    transaction_id: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

