import os
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)

    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
