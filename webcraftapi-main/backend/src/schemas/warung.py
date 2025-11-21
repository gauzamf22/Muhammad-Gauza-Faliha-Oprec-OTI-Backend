from pydantic import BaseModel, ConfigDict
from typing import Optional

class WarungCreate(BaseModel):
    name: str
    kantin_id: int
    owner_id: int
    image_url: str

class WarungUpdate(BaseModel):
    name: Optional[str] = None
    kantin_id: Optional[int] = None
    owner_id: Optional[int] = None
    image_url: Optional[str] = None

class WarungResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    kantin_id: Optional[int] = None
    owner_id: Optional[int] = None
    image_url: Optional[str] = None
