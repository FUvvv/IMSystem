# 📂 工程结构与环境配置整理

## 工程结构
```
Inventory-System/
├── backend/                  # Python 后端目录
│   ├── main.py               # 后端主程序入口 (路由与接口)
│   ├── database.py           # 数据库连接配置
│   ├── models.py             # 数据库模型 (SQLAlchemy)
│   ├── schemas.py            # 数据校验模型 (Pydantic)
│   └── requirements.txt      # Python 依赖包清单
├── frontend/                 # Vue3 前端目录
│   ├── index.html            # 页面入口
│   ├── package.json          # Node 依赖清单
│   ├── vite.config.js        # Vite 构建配置
│   └── src/
│       ├── main.js           # Vue主程序入口
│       ├── App.vue           # 根组件
│       ├── router/
│       │   └── index.js      # 路由配置
│       └── views/            # 页面视图
│           ├── Layout.vue          # 整体布局 (侧边栏+顶栏)
│           ├── Login.vue           # 登录页面 (完整功能)
│           ├── ProductManage.vue   # 商品管理 (完整功能)
│           ├── UserManage.vue      # 用户管理 (完整功能)
│           ├── InventoryManage.vue # 库存管理 (完整功能)
│           ├── LogManage.vue       # 日志管理 (完整功能)
│           ├── ReportManage.vue    # 报表管理 (完整功能)
│           ├── WarehouseManage.vue # 仓库管理 (仅UI)
│           ├── PurchaseManage.vue  # 采购管理 (仅UI)
│           └── SalesManage.vue     # 销售管理 (仅UI)
├── Readme.md
└── db.sql                    # 数据库初始化脚本
```

---

## 工程栈
- **Node.js (v18+)**：前端 Vue3 运行与构建环境  
- **Python (v3.9+)**：后端运行环境  
- **MySQL (v8.0+)**：本地数据库服务器  
- **Navicat**：数据库可视化管理工具  

---

## 数据库配置
- 数据库：`inventory_db`  
- 账号：`root`  
- 密码：`123456`  
- 端口：`3306`  
- 接口文件：`backend/database.py`  

---

## 后端环境配置
- **虚拟环境路径**：`xx\backend\venv\Scripts\activate`  
- **创建虚拟环境**：`python -m venv venv`  
- **启动虚拟环境**：`.venv\Scripts\activate`  
- **退出虚拟环境**：`deactivate`  
- **安装依赖**：`pip install -r requirements.txt`  

### requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
pydantic==2.5.2
cryptography==46.0.6
passlib[bcrypt]==1.7.4
```

### 后端启动
```bash
uvicorn main:app --reload
```
- 运行网址：`http://localhost:8000`  
- API 文档：`http://localhost:8000/docs`  

---

## 前端环境配置
- **路径**：`xx\frontend`  
- **初始化**：`npm install`  
- **启动**：`npm run dev`  
- **运行网址**：`http://localhost:3000`  

### package.json 依赖
```
@vitejs/plugin-vue@6.0.5
axios@1.14.0
echarts@5.6.0
element-plus@2.13.6
jspdf-autotable@5.0.7
jspdf@4.2.1
vite@8.0.3
vue-router@4.6.4
vue@3.5.31
xlsx@0.18.5
```

---

## 启动步骤
1. 使用 **Navicat** 连接数据库  
2. 新终端进入 `backend`，启动虚拟环境：  
   ```bash
   .venv\Scripts\activate
   uvicorn main:app --reload
   ```
3. 新终端进入 `frontend`，启动前端服务：  
   ```bash
   npm run dev
   ```
4. 浏览器访问：`http://localhost:3000`  

---

