from ...schemas.relationships.orderitem_menuitem import OrderItemWithDetailsResponse
from ...schemas.order import OrderResponse
from typing import List

class OrderWithDetailsResponse(OrderResponse):
    order_items: List[OrderItemWithDetailsResponse]