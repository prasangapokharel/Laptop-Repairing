from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from db import get_db
from models.payment import Payment
from models.order import Order
from schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentResponse, status_code=201)
async def create_payment(data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    order = await db.execute(select(Order).where(Order.id == data.order_id))
    if not order.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Order not found")
    
    payment = Payment(
        order_id=data.order_id,
        due_amount=data.due_amount,
        amount=data.amount,
        status=data.status,
        payment_method=data.payment_method,
        transaction_id=data.transaction_id
    )
    if data.status == "Paid":
        payment.paid_at = datetime.utcnow()
    
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


@router.get("", response_model=List[PaymentResponse])
async def list_payments(
    status: Optional[str] = Query(None),
    order_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Payment)
    if status:
        query = query.where(Payment.status == status)
    if order_id:
        query = query.where(Payment.order_id == order_id)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.patch("/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: int, data: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    if "status" in update_data and payment.status == "Paid" and not payment.paid_at:
        payment.paid_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(payment)
    return payment


@router.delete("/{payment_id}", status_code=204)
async def delete_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    await db.delete(payment)
    await db.commit()

