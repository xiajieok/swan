import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
from asset.utils import login_manager
from flask_restful import Api
from asset.api.urls  import restful_api

from config import config
from .ext import db
bootstrap = Bootstrap()
moment = Moment()
# db = SQLAlchemy()






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

    app.register_blueprint(restful_api)


    return app
