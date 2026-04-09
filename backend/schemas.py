from pydantic import BaseModel
from typing import Optional
from datetime import date
# --- 商品 ---
class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    specifications: Optional[str] = None
    produce_date: Optional[date] = None
    batch_number: Optional[str] = None
class ProductCreate(ProductBase): pass
class ProductUpdate(ProductBase): pass
class ProductResponse(ProductBase):
    id: int
    class Config: from_attributes = True
# --- 用户 ---
class UserLogin(BaseModel):
    username: str
    password: str
class UserRegister(BaseModel):
    username: str
    password: str
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
class UserUpdate(BaseModel):
    username: str
    role: str
    status: bool
class UserResetPassword(BaseModel):
    user_id: int

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    status: bool
    class Config: from_attributes = True

# --- 库存 ---
class InventoryUpdate(BaseModel):
    quantity_change: int # 正数为入库，负数为出库



