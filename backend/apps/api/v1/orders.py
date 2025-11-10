from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from decimal import Decimal
from db import get_db
from models.order import Order, OrderAssign
from schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderAssignCreate, OrderAssignResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db)):
    from models.device import Device
    
    device = await db.execute(select(Device).where(Device.id == data.device_id))
    if not device.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Device not found")
    
    total_cost = max(Decimal("0.00"), data.cost - data.discount)
    order = Order(
        device_id=data.device_id,
        customer_id=data.customer_id,
        problem_id=data.problem_id,
        cost=data.cost,
        discount=data.discount,
        total_cost=total_cost,
        note=data.note,
        status=data.status,
        estimated_completion_date=data.estimated_completion_date
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    status: Optional[str] = Query(None),
    customer_id: Optional[int] = Query(None),
    device_id: Optional[int] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if customer_id:
        query = query.where(Order.customer_id == customer_id)
    if device_id:
        query = query.where(Order.device_id == device_id)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, data: OrderUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    if "cost" in update_data or "discount" in update_data:
        order.total_cost = max(Decimal("0.00"), order.cost - order.discount)
    
    await db.commit()
    await db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await db.delete(order)
    await db.commit()
    return None


@router.post("/assign", response_model=OrderAssignResponse, status_code=201)
async def assign_order(data: OrderAssignCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(OrderAssign).where(
            OrderAssign.order_id == data.order_id,
            OrderAssign.user_id == data.user_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Order already assigned to this user")
    
    assign = OrderAssign(order_id=data.order_id, user_id=data.user_id)
    db.add(assign)
    await db.commit()
    await db.refresh(assign)
    return assign


@router.get("/assign/{order_id}", response_model=List[OrderAssignResponse])
async def get_order_assignments(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderAssign).where(OrderAssign.order_id == order_id))
    return result.scalars().all()

