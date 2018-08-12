import os
from flask import Flask
from asset import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# from config import DevelopmentConfig
from flask_failsafe import failsafe
# app = Flask(__name__)

# app.config.from_object(DevelopmentConfig)



manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run(default_command="runserver")
