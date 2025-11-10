from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from db import get_db
from models.device import DeviceType, Brand, Model, Device
from schemas.device import DeviceTypeCreate, DeviceTypeResponse, BrandCreate, BrandResponse, ModelCreate, ModelResponse, DeviceCreate, DeviceResponse, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/types", response_model=DeviceTypeResponse, status_code=201)
async def create_device_type(data: DeviceTypeCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(DeviceType).where(DeviceType.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Device type already exists")
    
    device_type = DeviceType(name=data.name, description=data.description)
    db.add(device_type)
    await db.commit()
    await db.refresh(device_type)
    return device_type


@router.get("/types", response_model=List[DeviceTypeResponse])
async def list_device_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DeviceType))
    return result.scalars().all()


@router.post("/brands", response_model=BrandResponse, status_code=201)
async def create_brand(data: BrandCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Brand).where(Brand.name == data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    brand = Brand(name=data.name)
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand


@router.get("/brands", response_model=List[BrandResponse])
async def list_brands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand))
    return result.scalars().all()


@router.post("/models", response_model=ModelResponse, status_code=201)
async def create_model(data: ModelCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Model).where(
            Model.brand_id == data.brand_id,
            Model.name == data.name,
            Model.device_type_id == data.device_type_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Model already exists")
    
    model = Model(brand_id=data.brand_id, name=data.name, device_type_id=data.device_type_id)
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model


@router.get("/models", response_model=List[ModelResponse])
async def list_models(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Model))
    return result.scalars().all()


@router.post("", response_model=DeviceResponse, status_code=201)
async def create_device(data: DeviceCreate, db: AsyncSession = Depends(get_db)):
    if data.serial_number:
        existing = await db.execute(select(Device).where(Device.serial_number == data.serial_number))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Serial number already exists")
    
    device = Device(
        brand_id=data.brand_id,
        model_id=data.model_id,
        device_type_id=data.device_type_id,
        serial_number=data.serial_number,
        owner_id=data.owner_id,
        notes=data.notes
    )
    db.add(device)
    await db.commit()
    await db.refresh(device)
    return device


@router.get("", response_model=List[DeviceResponse])
async def list_devices(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Device).limit(limit).offset(offset))
    return result.scalars().all()


@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.patch("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, data: DeviceUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
    
    await db.commit()
    await db.refresh(device)
    return device


@router.delete("/{device_id}", status_code=204)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device).where(Device.id == device_id))
    device = result.scalar_one_or_none()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    await db.delete(device)
    await db.commit()

