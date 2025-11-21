from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.warung import WarungCreate, WarungResponse, WarungUpdate
from ...schemas.relationships.warung_menuitem import WarungWithMenuResponse
from ...database.db import get_db
from ...models.model import Warung, User, Kantin

router = APIRouter()

# === GET ===
# tampilin smeua warung di ugm wkw
@router.get("/warung", response_model=list[WarungResponse])
def get_all_warung(db: Session = Depends(get_db)):
    warung = db.query(Warung).all()
    return warung

# Cari warung berdasarkan id (GET)
@router.get("/warung/{warung_id}", response_model=WarungWithMenuResponse)
def get_warung(warung_id: int, db: Session = Depends(get_db)):
    warung = db.query(Warung).filter(Warung.id == warung_id).first()
    
    if not warung:
        raise HTTPException(status_code=404, detail="Warung nggak ada")
    
    return warung

# Cari warung berdasarkan id kantinnya (GET)
@router.get("/kantin/{kantin_id}/warung", response_model=list[WarungWithMenuResponse])
def get_warung_by_kantin(kantin_id: int, db: Session = Depends(get_db)):
    warung_list = db.query(Warung).filter(Warung.kantin_id == kantin_id).all()
    
    if not warung_list:
        raise HTTPException(status_code=404, detail="Tidak ada warung di kantin ini")
    
    return warung_list

# Cari warung berdasarkan id ownernya (GET)
@router.get("/user/{owner_id}/warung", response_model=list[WarungResponse])
def get_warung_by_owner(owner_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User nggak ada")
    
    warung_list = db.query(Warung).filter(Warung.owner_id == owner_id).all()
    return warung_list


# === POST ===

# Nambah warung
@router.post("/warung", response_model=WarungResponse)
def create_warung(warung: WarungCreate, db: Session = Depends(get_db)):
    
    owner = db.query(User).filter(User.id == warung.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner nggak ada")
    
    
    kantin = db.query(Kantin).filter(Kantin.id == warung.kantin_id).first()
    if not kantin:
        raise HTTPException(status_code=404, detail="Kantin nggak ada")
    
    existing_warung = db.query(Warung).filter(
        Warung.name == warung.name,
        Warung.kantin_id == warung.kantin_id
    ).first()
    if existing_warung:
        raise HTTPException(status_code=400, detail="Warung dengan nama ini sudah ada di kantin ini!")
    
    new_warung = Warung(
        name=warung.name,
        owner_id=warung.owner_id,
        kantin_id=warung.kantin_id,
        image_url=warung.image_url
    )
    
    db.add(new_warung)
    db.commit()
    db.refresh(new_warung)
    
    return new_warung


# === PUT ===
# Update warung
@router.put("/warung/{warung_id}", response_model=WarungResponse)
def update_warung(
    warung_id: int, 
    warung_update: WarungUpdate, 
    db: Session = Depends(get_db)
):
    warung = db.query(Warung).filter(Warung.id == warung_id).first()
    
    if not warung:
        raise HTTPException(status_code=404, detail="Warung not found")
    
    if warung_update.kantin_id:
        kantin = db.query(Kantin).filter(Kantin.id == warung_update.kantin_id).first()
        if not kantin:
            raise HTTPException(status_code=404, detail="Kantin nggak ada")
    
    if warung_update.owner_id:
        owner = db.query(User).filter(User.id == warung_update.owner_id).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner nggak ada")
    
    warung.name = warung_update.name
    warung.owner_id = warung_update.owner_id
    warung.kantin_id = warung_update.kantin_id
    warung.image_url = warung_update.image_url
    
    db.commit()
    db.refresh(warung)
    
    return warung


# === DELETE ===

# Hapus kantin berdasarkan id 
@router.delete("/warung/{warung_id}")
def delete_warung(warung_id: int, db: Session = Depends(get_db)):
    warung = db.query(Warung).filter(Warung.id == warung_id).first()
    
    if not warung:
        raise HTTPException(status_code=404, detail="Warung nggak ada")
    
    db.delete(warung)
    db.commit()
    
    return {"message": f"Warung {warung_id}, berhasil dihapus"}