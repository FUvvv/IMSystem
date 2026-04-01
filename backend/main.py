from fastapi import FastAPI, Depends
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

# --- 商品管理接口 ---
@app.get("/api/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 自动生成对应的库存条目
    db_inv = models.Inventory(product_id=db_product.id, quantity=0)
    db.add(db_inv)
    
    # 记录日志
    db_log = models.Log(user="admin", action=f"新增商品: {product.name}", type="操作")
    db.add(db_log)
    db.commit()
    return db_product

# --- 日志查询接口 ---
@app.get("/api/logs", response_model=list[schemas.LogResponse])
def get_logs(db: Session = Depends(get_db)):
    return db.query(models.Log).order_by(models.Log.id.desc()).all()
