from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    password: str
    profile_picture: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[str]
    profile_picture: Optional[str]
    is_active: bool
    is_staff: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RoleEnrollCreate(BaseModel):
    user_id: int
    role_id: int


class RoleEnrollResponse(BaseModel):
    id: int
    user_id: int
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True

