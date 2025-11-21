from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from ...database.db import get_db
from ...models.model import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from dotenv import load_dotenv
from ...schemas.login import LoginRequest, LoginResponse
from ...schemas.users import UserResponse, UserCreate

# OAuth2PasswordBearer, dibuat full sama chatgpt wkw, ga sempettt

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Fallback for development, but warn
    SECRET_KEY = "insecure-default-key-change-me"
    print("WARNING: Using default SECRET_KEY. This is insecure for production!")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

router = APIRouter()

# Utility functions
def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user



# ====================== AUTH ENDPOINTS ===========================


@router.post("/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    print("goes thru")
    if not user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "name": user.name
    }

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    print("Registered!")
    
    password_hash = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=password_hash,
        name=user.name,
        phone_number=user.phone_number
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

