"""
应用初始化模块

该模块负责Flask应用程序的创建和配置。它实现了工厂模式，通过create_app函数创建和配置
Flask应用实例。

流程概述:
1. 创建Flask应用实例，配置模板和静态文件路径
2. 配置数据库连接、密钥和文件上传相关设置
3. 初始化扩展(SQLAlchemy, Migrate)
4. 注册蓝图组件，实现模块化路由管理

组件说明:
- db: SQLAlchemy实例，用于ORM数据库操作
- migrate: Flask-Migrate实例，用于数据库迁移管理
- blueprint组件:
  - material_bp: 材料管理模块
  - customer_bp: 客户管理模块
  - supplier_bp: 供应商管理模块

配置项:
- SQLALCHEMY_DATABASE_URI: 数据库连接URI
- SQLALCHEMY_TRACK_MODIFICATIONS: 是否跟踪对象变化
- SECRET_KEY: 应用密钥，用于会话安全
- UPLOAD_FOLDER: 文件上传目录路径
- MAX_CONTENT_LENGTH: 上传文件大小限制
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from .views.material_views import material_bp
    app.register_blueprint(material_bp, url_prefix='/material')
    
    from .customer.routes import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')

    from .supplier.routes import bp as supplier_bp
    app.register_blueprint(supplier_bp, url_prefix='/supplier')

    # 导入路由
    from . import routes
    routes.init_app(app)

    return app