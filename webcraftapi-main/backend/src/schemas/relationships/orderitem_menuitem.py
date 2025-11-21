from ...schemas.orderitem import OrderItemResponse
from ...schemas.menuitem import MenuItemResponse

class OrderItemWithDetailsResponse(OrderItemResponse):
    menu_item: MenuItemResponse