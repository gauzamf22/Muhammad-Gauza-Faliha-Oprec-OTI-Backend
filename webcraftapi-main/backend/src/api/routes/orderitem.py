from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.orderitem import OrderItemCreate, OrderItemResponse, OrderItemUpdate
from ...schemas.relationships.orderitem_menuitem import OrderItemWithDetailsResponse
from ...database.db import get_db
from ...models.model import OrderItem, MenuItem
from typing import List

router = APIRouter()

# ====================== API ENDPOINTSSS pada tabel OrderItem (item yg diorder) ===========================

# === GET ===

# Nampilin semua order item (isi tabel orderitem) (GET) 
@router.get("/order-items", response_model=List[OrderItemResponse])
def get_all_order_items(db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).all()
    return order_items

# Cari order item berdasarkan order item id (GET)
@router.get("/order-items/{order_item_id}", response_model=OrderItemWithDetailsResponse)
def get_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item nggak ada")
    
    return order_item

# Cari order item berdasarkan order id
@router.get("/orders/{order_id}/items", response_model=List[OrderItemWithDetailsResponse])
def get_order_items_by_order(order_id: int, db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return order_items

# cari order item berdasarkan menu item id
@router.get("/menu-items/{menu_item_id}/order-items", response_model=List[OrderItemResponse])
def get_order_items_by_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    order_items = db.query(OrderItem).filter(OrderItem.menu_item_id == menu_item_id).all()
    return order_items


# === POST ===

# membuat order itme baru
@router.post("/order-items", response_model=OrderItemResponse)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):

    menu_item = db.query(MenuItem).filter(MenuItem.id == order_item.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item nggak ada")
    
    if menu_item.stock < order_item.quantity:
        raise HTTPException(status_code=400, detail="Stok menu item tidak cukup")
    
    new_order_item = OrderItem(
        order_id=order_item.order_id,
        menu_item_id=order_item.menu_item_id,
        quantity=order_item.quantity,
        price_at_purchase=order_item.price_at_purchase
    )
    
    menu_item.stock -= order_item.quantity
    
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    
    return new_order_item


# === PUT ===
# Update order item
# ini yg buat deepseek, aku gak tau isinya apa wkw
@router.put("/order-items/{order_item_id}", response_model=OrderItemResponse)
def update_order_item(
    order_item_id: int, 
    order_item_update: OrderItemUpdate, 
    db: Session = Depends(get_db)
):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item nggak ada")
    
    if order_item_update.quantity is not None and order_item_update.quantity != order_item.quantity:
        menu_item = db.query(MenuItem).filter(MenuItem.id == order_item.menu_item_id).first()
        if menu_item:
            stock_diff = order_item.quantity - order_item_update.quantity
            menu_item.stock += stock_diff
            
            if menu_item.stock < 0:
                raise HTTPException(status_code=400, detail="Stok tidak cukup untuk perubahan ini")
    
    # Update fields
    if order_item_update.order_id is not None:
        order_item.order_id = order_item_update.order_id
    if order_item_update.menu_item_id is not None:
        order_item.menu_item_id = order_item_update.menu_item_id
    if order_item_update.quantity is not None:
        order_item.quantity = order_item_update.quantity
    if order_item_update.price_at_purchase is not None:
        order_item.price_at_purchase = order_item_update.price_at_purchase
    
    db.commit()
    db.refresh(order_item)
    
    return order_item


# === DELETE ===

# Hapus order item berdasarkan id 
@router.delete("/order-items/{order_item_id}")
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    order_item = db.query(OrderItem).filter(OrderItem.id == order_item_id).first()
    
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item nggak ada")
    
    # Restore stock when deleting order item
    menu_item = db.query(MenuItem).filter(MenuItem.id == order_item.menu_item_id).first()
    if menu_item:
        menu_item.stock += order_item.quantity
    
    db.delete(order_item)
    db.commit()
    
    return {"message": f"Order item {order_item_id} berhasil dihapus"}