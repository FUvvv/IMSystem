
工程结构
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

工程栈
    Node.js (v18+)：作为前端Vue3的运行和构建环境。
    Python (v3.9+)：作为后端运行环境。
    MySQL (v8.0+)：本地数据库服务器。
    Navicat：数据库可视化管理工具。

本地数据库：inventory_db
    账号：root
    密码：123456
    端口：3306
    代码接口：database.py

环境配置：
后端：python虚拟环境
    路径：xx\backend\venv\Scripts\activate
    创建：python -m venv venv
    启动：.venv\Scripts\activate
    退出：deactivate
    配置：pip install -r requirements.txt
        fastapi==0.104.1
        uvicorn==0.24.0
        sqlalchemy==2.0.23
        pymysql==1.1.0
        pydantic==2.5.2
    后端启动代码：uvicorn main:app --reload
    后端运行网址： http://localhost:8000
    api接口文档反馈： http://localhost:8000/docs
前端：Vue 3
    路径：xx\frontend
    初始化：npm install
    启动：npm run dev
    运行网址： http://localhost:3000
    配置： inventory-frontend@0.0.0 G:\AAA IMSystem\1.2\frontend
            +-- @vitejs/plugin-vue@6.0.5
            +-- axios@1.14.0
            +-- echarts@5.6.0
            +-- element-plus@2.13.6
            +-- vite@8.0.3
            +-- vue-router@4.6.4
            +-- vue@3.5.31
            `-- xlsx@0.18.5
启动步骤：
    1、navicat连接数据库
    2、新终端，cd backend，启动虚拟环境：.venv\Scripts\activate，启动后端服务：uvicorn main:app --reload
    3、新终端，cd frontend，启动前端服务：npm run dev
    4、浏览器打开：http://localhost:3000


