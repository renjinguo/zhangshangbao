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

    # 导入路由
    from . import routes
    routes.init_app(app)

    return app