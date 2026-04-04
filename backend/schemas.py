from pydantic import BaseModel
from typing import Optional

# --- 商品 ---
class ProductBase(BaseModel):
    name: str
    category: str
    price: float

class ProductCreate(ProductBase): pass
class ProductUpdate(ProductBase): pass
class ProductResponse(ProductBase):
    id: int
    class Config: from_attributes = True

# --- 用户 ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserUpdate(BaseModel):
    username: str
    role: str
    status: bool
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    status: bool
    class Config: from_attributes = True

# --- 库存 ---
class InventoryUpdate(BaseModel):
    quantity_change: int # 正数为入库，负数为出库

# --- 登录 ---
class UserLogin(BaseModel):
    username: str
    password: str


