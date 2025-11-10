from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base


class DeviceType(Base):
    __tablename__ = "device_types"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    models = relationship("Model", back_populates="device_type", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="device_type")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    models = relationship("Model", back_populates="brand", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="brand")


class Model(Base):
    __tablename__ = "models"

    id = Column(BigInteger, primary_key=True)
    brand_id = Column(BigInteger, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    device_type_id = Column(BigInteger, ForeignKey("device_types.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    brand = relationship("Brand", back_populates="models")
    device_type = relationship("DeviceType", back_populates="models")
    devices = relationship("Device", back_populates="model")

    __table_args__ = (UniqueConstraint("brand_id", "name", "device_type_id"),)


class Device(Base):
    __tablename__ = "devices"

    id = Column(BigInteger, primary_key=True)
    brand_id = Column(BigInteger, ForeignKey("brands.id", ondelete="RESTRICT"), nullable=False, index=True)
    model_id = Column(BigInteger, ForeignKey("models.id", ondelete="RESTRICT"), nullable=False, index=True)
    device_type_id = Column(BigInteger, ForeignKey("device_types.id", ondelete="RESTRICT"), nullable=False, index=True)
    serial_number = Column(String(100), unique=True, index=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    brand = relationship("Brand", back_populates="devices")
    model = relationship("Model", back_populates="devices")
    device_type = relationship("DeviceType", back_populates="devices")

