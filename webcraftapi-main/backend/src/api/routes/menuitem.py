from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.menuitem import MenuItemCreate, MenuItemResponse, MenuItemUpdate
from ...database.db import get_db
from ...models.model import MenuItem, Kantin
from decimal import Decimal

router = APIRouter()

# ====================== API ENDPOINTSSS pada tabel MenuItem ===========================

# === GET ===

# Nampilin semua menu item (isi tabel MenuItem) (GET) 
@router.get("/menuitem", response_model=list[MenuItemResponse])
def get_all_menuitem(db: Session = Depends(get_db)):
    users = db.query(MenuItem).all()
    return users

# Cari menu item berdasarkan id (GET)
@router.get("/menuitem/{menuitem_id}", response_model=MenuItemResponse)
def get_menuitem(menuitem_id: int, db: Session = Depends(get_db)):
    menuitem = db.query(MenuItem).filter(MenuItem.id == menuitem_id).first()
    
    if not menuitem:
        raise HTTPException(status_code=404, detail="MenuItem nggak ada")
    
    return menuitem

# Cari item menu berdasarkan warung
@router.get("/warung/{warung_id}/menu", response_model=MenuItemResponse)
def get_menuitem_by_kantin(warung_id: int, db: Session = Depends(get_db)):
    menuitem = db.query(MenuItem).filter(Kantin.id == warung_id).first()
    
    if not menuitem:
        raise HTTPException(status_code=404, detail="MenuItem nggak ada")
    
    return menuitem

# Cari menu item berdasarkan query paramter (nama atau harga) (GET)
@router.get("/menuitem/", response_model=MenuItemResponse)
def get_menuitem_by_query(name: str = None, price: Decimal = None, db: Session = Depends(get_db)):
    if name:
        menuitem = db.query(MenuItem).filter(MenuItem.name == name).first()
    elif price:
        menuitem = db.query(MenuItem).filter(MenuItem.price == price).first()
    else:
        raise HTTPException(status_code=400, detail="Mohon berikan paramater 'price' atau 'name'")
    
    if not menuitem:
        raise HTTPException(status_code=404, detail="MenuItem nggak ada")
    return menuitem


# === POST ===

# Nambah item menu
@router.post("/menuitem", response_model=MenuItemResponse)
def create_menuitem(menuitem: MenuItemCreate, db: Session = Depends(get_db)):

    # existing_menuitem = db.query(MenuItem).filter(MenuItem.id == menuitem.id).first()
    # if existing_menuitem:
    #     raise HTTPException(status_code=400, detail="Item menu sudah ada!")
    
    new_menuitem = MenuItem(
        warung_id=menuitem.warung_id,
        name=menuitem.name,
        price=menuitem.price,
        image_url=menuitem.image_url,
        stock=menuitem.stock
    )
    
    db.add(new_menuitem)
    db.commit()
    db.refresh(new_menuitem)  
    
    return new_menuitem


# === PUT ===
# Update item menu
@router.put("/menuitem/{menuitem_id}", response_model=MenuItemResponse)
def update_user(
    menuitem_id: int, 
    menuitem_update: MenuItemUpdate, 
    db: Session = Depends(get_db)
):
    user = db.query(MenuItem).filter(MenuItem.id == menuitem_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="MenuItem not found")
    
    user.name = menuitem_update.name
    
    db.commit()
    db.refresh(user)
    
    return user


# === DELETE ===

# Hapus user berdasarkan id 
@router.delete("/menuitem/{user_id}")
def delete_menuitemr(menuitem_id: int, db: Session = Depends(get_db)):
    menuitem = db.query(MenuItem).filter(MenuItem.id == menuitem_id).first()
    
    if not menuitem:
        raise HTTPException(status_code=404, detail="MenuItem nggak ada")
    
    db.delete(menuitem)
    db.commit()
    
    return {"message": f"MenuItem {menuitem_id} berhasil dihapus"}