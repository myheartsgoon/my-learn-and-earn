from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .controllers import bp
from .configs import config


def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'

    # create flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # init db models
    db.init_app(app)

    # init login manager with app
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = "blog.login"
    login_manager.login_message = "该页面需要登陆"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprints
    app.register_blueprint(bp)

    return app
