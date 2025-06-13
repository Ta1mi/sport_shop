from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    full_name: str
    role: str

@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None
    image_url: Optional[str] = None

@dataclass
class Order:
    id: int
    user_id: int
    total_amount: float
    status: str