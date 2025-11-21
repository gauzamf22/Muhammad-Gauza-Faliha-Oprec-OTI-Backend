from pydantic import BaseModel, ConfigDict
from typing import Optional

class KantinCreate(BaseModel):
    name: str
    description: str
    location: str
    image_url: str

class KantinUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None

class KantinResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str
    location: str
    image_url: str
