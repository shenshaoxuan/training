from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()



def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    migrate.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    # 指定提示信息（默认时英文的）
    login_manager.login_message = '登录后才可访问'


