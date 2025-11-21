from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.kantin import KantinCreate, KantinResponse, KantinUpdate
from ...database.db import get_db
from ...models.model import Kantin

router = APIRouter()

# ====================== API ENDPOINTSSS pada tabel Kantin ===========================

# === GET ===
# tampilin smeua kantin di ugm
@router.get("/kantin", response_model=list[KantinResponse])
def get_all_kantin(db: Session = Depends(get_db)):
    kantin = db.query(Kantin).all()
    return kantin

# Cari kantin berdasarkan id (GET)
@router.get("/kantin/{kantin_id}", response_model=KantinResponse)
def get_kantin(kantin_id: int, db: Session = Depends(get_db)):
    kantin = db.query(Kantin).filter(Kantin.id == kantin_id).first()
    
    if not kantin:
        raise HTTPException(status_code=404, detail="Kantin nggak ada")
    
    return kantin

# Cari kantin berdasarkan query paramter (nama atau location) (GET)
@router.get("/kantin/", response_model=KantinResponse)
def get_kantin_by_query(name: str = None, location: str = None, db: Session = Depends(get_db)):
    if name:
        kantin = db.query(Kantin).filter(Kantin.name == name).first()
    elif location:
        kantin = db.query(Kantin).filter(Kantin.lolocation ==location).first()
    else:
        raise HTTPException(status_code=400, detail="Mohon berikan paramater 'location' atau 'name'")
    
    if not kantin:
        raise HTTPException(status_code=404, detail="Kantin nggak ada")
    return kantin


# === POST ===

# Nambah kantin 
@router.post("/kantin", response_model=KantinResponse)
def create_kantin(kantin: KantinCreate, db: Session = Depends(get_db)):

    existing_kantin = db.query(Kantin).filter(Kantin.name == kantin.name).first()
    if existing_kantin:
        raise HTTPException(status_code=400, detail="Kantin sudah ada!")
    
    new_kantin = Kantin(
        name=kantin.name,
        location=kantin.location,
        description=kantin.description,
        image_url=kantin.image_url
    )
    
    db.add(new_kantin)
    db.commit()
    db.refresh(new_kantin)  
    
    return new_kantin


# === PUT ===
# Update kantin
@router.put("/kantin/{kantin_id}", response_model=KantinResponse)
def update_kantin(
    kantin_id: int, 
    kantin_update: KantinUpdate, 
    db: Session = Depends(get_db)
):
    kantin = db.query(Kantin).filter(Kantin.id == kantin_id).first()
    
    if not kantin:
        raise HTTPException(status_code=404, detail="Kantin not found")
    
    kantin.name = kantin_update.name
    kantin.location = kantin_update.location
    kantin.description = kantin_update.description
    kantin.image_url = kantin_update.image_url
    
    db.commit()
    db.refresh(kantin)
    
    return kantin


# === DELETE ===

# Hapus kantin berdasarkan id 
@router.delete("/kantin/{kantin_id}")
def delete_kantin(kantin_id: int, db: Session = Depends(get_db)):
    kantin = db.query(Kantin).filter(Kantin.id == kantin_id).first()
    
    if not kantin:
        raise HTTPException(status_code=404, detail="Kantin nggak ada")
    
    db.delete(kantin)
    db.commit()
    
    return {"message": f"Kantin {kantin_id}, berhasil dihapus"}