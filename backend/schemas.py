from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    category: str
    price: float

class ProductCreate(ProductBase): pass
class ProductResponse(ProductBase):
    id: int
    class Config: from_attributes = True

class LogResponse(BaseModel):
    id: int
    user: str
    action: str
    type: str
    class Config: from_attributes = True
