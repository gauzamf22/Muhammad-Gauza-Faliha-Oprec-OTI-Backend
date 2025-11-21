from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ...schemas.users import UserCreate, UserResponse, UserUpdate
from ...database.db import get_db
from ...models.model import User
from ...api.routes.authentication import get_password_hash

router = APIRouter()

# ====================== API ENDPOINTSSS pada tabel USER ===========================

# === GET ===

# Nampilin semua user (isi tabel Users) (GET) 
@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Cari user berdasarkan id (GET)
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User nggak ada")
    
    return user

# Cari user berdasarkan query paramter (nama atau email) (GET)
@router.get("/users/", response_model=UserResponse)
def get_user_by_query(
    name: str = None, 
    email: str = None, 
    db: Session = Depends(get_db),
):
    if name:
        user = db.query(User).filter(User.name == name).first()
    elif email:
        user = db.query(User).filter(User.email == email).first()
    else:
        raise HTTPException(status_code=400, detail="Mohon berikan paramater 'email' atau 'name'")
    
    if not user:
        raise HTTPException(status_code=404, detail="User nggak ada")
    return user

# === POST ===

# Nambah user 
@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email sudah ada!")
    
    password_hash = get_password_hash(user.password)
    
    new_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        password_hash=password_hash,
        phone_number=user.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  
    
    return new_user

# === PUT ===
# Update user
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = user_update.name
    user.email = user_update.email
    user.role = user_update.role
    user.phone_number = user_update.phone_number
    
    # If password is being updated, hash it
    if user_update.password:
        user.password_hash = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(user)
    
    return user

# === DELETE ===

# Hapus user berdasarkan id 
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User nggak ada")
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user_id} berhasil dihapus"}