import os
from flask import g
from asset import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

import logging

from flask_login import current_user

app = create_app('development')
manager = Manager(app)


@app.before_request
def before_request():
    g.user = current_user


manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run(default_command="runserver")
