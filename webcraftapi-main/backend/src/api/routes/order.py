from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.order import OrderUpdate, OrderCreate, OrderResponse
from ...schemas.relationships.order_detail import OrderWithDetailsResponse
from ...database.db import get_db
from ...models.model import Order, OrderItem
from typing import List
from datetime import datetime

router = APIRouter()

# ====================== API ENDPOINTSSS pada tabel Order ===========================

# === GET ===

# Nampilin semua order (isi tabel Order) (GET) 
@router.get("/orders", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

# Cari order berdasarkan id (GET)
@router.get("/orders/{order_id}", response_model=OrderWithDetailsResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order nggak ada")
    
    return order

# Cari order berdasarkan user id
@router.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

# Cari order berdasarkan warung id
@router.get("/warung/{warung_id}/orders", response_model=List[OrderResponse])
def get_orders_by_warung(warung_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.warung_id == warung_id).all()
    return orders

# Cari order berdasarkan payment status
@router.get("/orders/status/{payment_status}", response_model=List[OrderResponse])
def get_orders_by_status(payment_status: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.payment_status == payment_status).all()
    return orders


# === POST ===

# Nambah order 
@router.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """
    Create an order and all of its order items in one request.
    """
    # Create main order
    new_order = Order(
        user_id=order_data.user_id,
        warung_id=order_data.warung_id,
        total_price=order_data.total_price,
        payment_status=order_data.payment_status or "pending",
        created_at=order_data.created_at or datetime.utcnow(),
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add order items if present
    if getattr(order_data, "order_items", None):
        for item in order_data.order_items:
            new_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price_at_purchase=item.price_at_purchase,
            )
            db.add(new_item)

        db.commit()
        db.refresh(new_order)

    return new_order


# === PUT )===
# Update order
@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order nggak ada")

    for field, value in order_update.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order

# Update order payment status
@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    payment_status: str, 
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order nggak ada")
    
    order.payment_status = payment_status
    db.commit()
    db.refresh(order)
    
    return order


# === DELETE ===

# Hapus order berdasarkan id (padahal kyknya gaakan pernah kepake)
@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order nggak ada")
    
    db.delete(order)
    db.commit()
    
    return {"message": f"Order {order_id} berhasil dihapus"}