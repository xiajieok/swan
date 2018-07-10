import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api,Resource
from asset.apis import views as apis

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'




def create_app(config_name):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    api = Api(app)
    api.add_resource(api.HelloWorld, '/api')


    return app
