from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price: float
    description: Optional[str] = None
    category: str  # apericena, bevande, vini, mixology, gin
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MenuItemCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: str

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class MenuCategory(BaseModel):
    id: str
    label: str
    icon: str
    items: List[MenuItem] = []