from ..warung import WarungResponse
from ..menuitem import MenuItemResponse
from typing import List

class WarungWithMenuResponse(WarungResponse):
    menu_items: List[MenuItemResponse]