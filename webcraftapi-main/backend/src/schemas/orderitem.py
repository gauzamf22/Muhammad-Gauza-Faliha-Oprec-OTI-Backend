from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

class OrderItemCreate(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int
    price_at_purchase: Decimal

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    quantity: Optional[int] = None
    price_at_purchase: Optional[Decimal] = None

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    price_at_purchase: Decimal