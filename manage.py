import os
from flask import g
from asset import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask import jsonify
from asset import models
from asset.utils import login_manager
from flask_login import current_user

app = create_app('development')
manager = Manager(app)


@app.before_request
def before_request():
    g.user = current_user


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

manager.add_command('db', MigrateCommand)
#
# from flask_httpauth import HTTPBasicAuth
#
# auth = HTTPBasicAuth()
#
# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = models.User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = models.User.query.filter_by(username = username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True




if __name__ == '__main__':
    manager.run(default_command="runserver")
