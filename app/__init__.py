import os
from flask import Flask
from .models import db
from .routes.recipe_routes import recipe_bp

def create_app(test_config=None):
    # 建立 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'database.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        # 覆蓋預設設定 (如果有的話)
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在，用於存放 SQLite 資料庫
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化 SQLAlchemy 套件
    db.init_app(app)

    # 在啟動前自動建立資料表
    with app.app_context():
        db.create_all()

    # 註冊路由 Blueprint
    app.register_blueprint(recipe_bp)

    return app
