from flask import Flask

from app.extensions import config_extensions



def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.settings')
    app.config.from_object('app.config.secure')
    config_extensions(app)
    register_blueprint(app)
    return app

def register_blueprint(app):
    from app.api.v1.user import user
    from app.api.v1.main import main
    from app.api.v1.course import course
    from app.api.v1.vote import vote

    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(course)
    app.register_blueprint(vote)






