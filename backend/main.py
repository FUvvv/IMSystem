from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext  # 新增导入
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# 配置 Bcrypt 哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 辅助函数：生成密码哈希
def get_password_hash(password: str):
    return pwd_context.hash(password)
# 辅助函数：校验密码
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ================= 权限与日志核心 =================
def get_current_user(x_username: str = Header(default=None), db: Session = Depends(get_db)):
    if not x_username:
        raise HTTPException(status_code=401, detail="未提供身份凭证，请重新登录")
    user = db.query(models.User).filter(models.User.username == x_username).first()
    if not user or not user.status:
        raise HTTPException(status_code=403, detail="账号无效或已被禁用")
    return user

def record_log(db: Session, user: str, action: str, log_type: str = "操作"):
    db_log = models.Log(user=user, action=action, type=log_type)
    db.add(db_log)
    db.commit()

# ================= 业务接口 =================

# 1. 登录接口 (校验哈希)
@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    # 使用 verify_password 校验明文密码与数据库中的哈希值
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
        
    if not db_user.status:
        raise HTTPException(status_code=403, detail="该账号已被禁用")
    
    record_log(db, user.username, "用户登录系统", "登录")
    return {"msg": "登录成功", "token": f"mock_token_{db_user.id}", "username": db_user.username, "role": db_user.role}

# 2. 注册接口 (加密存储)
@app.post("/api/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    exist_user = db.query(models.User).filter(models.User.username == user.username).first()
    if exist_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
        
    # 存储哈希后的密码
    hashed_pwd = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_pwd, role="user", status=True)
    db.add(db_user)
    db.commit()
    return {"msg": "注册成功"}

# --- 商品接口 ---
@app.get("/api/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.add(models.Inventory(product_id=db_product.id, quantity=0))
    # 使用真实登录的用户名记录日志
    record_log(db, current_user.username, f"新增商品: {product.name}")
    db.commit()
    return db_product

@app.put("/api/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    record_log(db, current_user.username, f"修改商品信息: {product.name}")
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(models.Inventory).filter(models.Inventory.product_id == product_id).delete()
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        record_log(db, current_user.username, f"删除商品: {db_product.name}")
        db.delete(db_product)
        db.commit()
    return {"msg": "删除成功"}

@app.get("/api/products", response_model=list[schemas.ProductResponse])
def get_products(search: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if search:
        # 模糊匹配名称或分类
        query = query.filter((models.Product.name.contains(search)) | (models.Product.category.contains(search)))
    return query.all()

# --- 库存接口 ---
@app.get("/api/inventory")
def get_inventory(db: Session = Depends(get_db)):
    res = db.query(models.Inventory, models.Product.name).join(models.Product).all()
    return [{"id": inv.id, "product_id": inv.product_id, "product_name": name, "quantity": inv.quantity, "min_alert": inv.min_alert} for inv, name in res]

@app.put("/api/inventory/{inv_id}")
def update_inventory(inv_id: int, inv_update: schemas.InventoryUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_inv = db.query(models.Inventory).filter(models.Inventory.id == inv_id).first()
    db_product = db.query(models.Product).filter(models.Product.id == db_inv.product_id).first()
    db_inv.quantity += inv_update.quantity_change
    action_name = "入库" if inv_update.quantity_change > 0 else "出库"
    # 使用真实登录的用户名记录日志
    record_log(db, current_user.username, f"商品[{db_product.name}] {action_name} {abs(inv_update.quantity_change)} 件")
    db.commit()
    return {"msg": "更新成功"}

# --- 用户与日志接口 ---
@app.get("/api/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# 新增用户 (加密存储)
@app.post("/api/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = get_password_hash(user.password)
    # 替换明文密码为哈希值
    db_user = models.User(username=user.username, password=hashed_pwd, role=user.role, status=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/api/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.username = user.username
    db_user.role = user.role
    db_user.status = user.status
    if user.password: db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# --- 管理员重置密码 ---
@app.post("/api/users/reset_password")
def reset_password(req: schemas.UserResetPassword, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="仅管理员可重置密码")
    db_user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    # 将重置的默认密码 123456 进行哈希加密后存入数据库
    db_user.password = get_password_hash("123456")
    record_log(db, current_user.username, f"重置用户[{db_user.username}]密码为默认密码")
    db.commit()
    return {"msg": "密码已重置为123456"}

@app.get("/api/logs")
def get_logs(user: str = None, type: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Log)
    if user: query = query.filter(models.Log.user.contains(user))
    if type: query = query.filter(models.Log.type == type)
    return query.order_by(models.Log.id.desc()).all()

# --- 报表接口 (加入权限校验) ---
@app.get("/api/dashboard")
def get_dashboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 核心：校验必须是 admin 角色
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="权限不足，仅管理员可查看报表数据")
        
    product_count = db.query(models.Product).count()
    low_stock_count = db.query(models.Inventory).filter(models.Inventory.quantity < models.Inventory.min_alert).count()
    cat_stats = db.query(models.Product.category, func.count(models.Product.id).label('count'), func.avg(models.Product.price).label('avg_price')).group_by(models.Product.category).all()
    product_stats = [{"category": c[0], "count": c[1], "avgPrice": round(float(c[2]), 2) if c[2] else 0} for c in cat_stats]
    inv_res = db.query(models.Inventory, models.Product.name).join(models.Product).all()
    inventory_stats = [{"name": name, "stock": inv.quantity, "min_alert": inv.min_alert} for inv, name in inv_res]
    
    return {
        "summary": { "product_count": product_count, "low_stock_count": low_stock_count },
        "product_stats": product_stats,
        "inventory_stats": inventory_stats
    }
