from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class OrderCreate(BaseModel):
    device_id: int
    customer_id: Optional[int] = None
    problem_id: Optional[int] = None
    cost: Decimal = Decimal("0.00")
    discount: Decimal = Decimal("0.00")
    note: Optional[str] = None
    status: str = "Pending"
    estimated_completion_date: Optional[datetime] = None


class OrderUpdate(BaseModel):
    device_id: Optional[int] = None
    customer_id: Optional[int] = None
    problem_id: Optional[int] = None
    cost: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    note: Optional[str] = None
    status: Optional[str] = None
    estimated_completion_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class OrderResponse(BaseModel):
    id: int
    device_id: int
    customer_id: Optional[int]
    problem_id: Optional[int]
    cost: Decimal
    discount: Decimal
    total_cost: Decimal
    note: Optional[str]
    status: str
    estimated_completion_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderAssignCreate(BaseModel):
    order_id: int
    user_id: int


class OrderAssignResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True

