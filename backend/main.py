from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= 商品管理 =================
@app.get("/api/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 同步创建库存条目
    db_inv = models.Inventory(product_id=db_product.id, quantity=0)
    db.add(db_inv)
    db.commit()
    return db_product

@app.put("/api/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product: raise HTTPException(status_code=404, detail="商品不存在")
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # 先删除关联库存
    db.query(models.Inventory).filter(models.Inventory.product_id == product_id).delete()
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return {"msg": "删除成功"}

# ================= 库存管理 =================
@app.get("/api/inventory")
def get_inventory(db: Session = Depends(get_db)):
    res = db.query(models.Inventory, models.Product.name).join(models.Product).all()
    return [{"id": inv.id, "product_id": inv.product_id, "product_name": name, "quantity": inv.quantity, "min_alert": inv.min_alert} for inv, name in res]

@app.put("/api/inventory/{inv_id}")
def update_inventory(inv_id: int, inv_update: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    db_inv = db.query(models.Inventory).filter(models.Inventory.id == inv_id).first()
    if not db_inv: raise HTTPException(status_code=404, detail="库存记录不存在")
    db_inv.quantity += inv_update.quantity_change
    if db_inv.quantity < 0: raise HTTPException(status_code=400, detail="库存不足")
    db.commit()
    return {"msg": "库存更新成功", "current_quantity": db_inv.quantity}

# ================= 用户管理 =================
@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/api/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user: raise HTTPException(status_code=404, detail="用户不存在")
    
    db_user.username = user.username
    db_user.role = user.role
    db_user.status = user.status
    if user.password: # 如果传了新密码则更新
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user
    
@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # 查询数据库中的用户
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    # 校验账号与密码
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    # 校验账号状态
    if not db_user.status:
        raise HTTPException(status_code=403, detail="该账号已被禁用，请联系管理员")
        
    # 返回登录成功信息与模拟Token
    return {
        "msg": "登录成功",
        "token": f"mock_token_user_{db_user.id}",
        "username": db_user.username,
        "role": db_user.role
    }
