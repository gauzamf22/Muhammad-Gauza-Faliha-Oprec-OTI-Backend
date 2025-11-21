from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

class OrderItemCreate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: int
    quantity: int
    price_at_purchase: Decimal

class OrderCreate(BaseModel):
    user_id: int
    warung_id: int
    total_price: Decimal
    payment_status: Optional[str] = "pending"
    created_at: Optional[datetime] = None
    order_items: Optional[List[OrderItemCreate]] = []

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    warung_id: Optional[int] = None
    total_price: Optional[Decimal] = None
    payment_status: Optional[str] = None
    created_at: Optional[datetime] = None

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    warung_id: int
    total_price: Decimal
    payment_status: str
    created_at: Optional[datetime]


