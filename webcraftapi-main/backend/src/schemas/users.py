from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "customer"
    password: str
    phone_number: Optional[str] = None

class UserUpdate(BaseModel):
    name: str = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    role: Optional[str] = "customer"
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True