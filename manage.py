import os
from asset import create_app, db
from flask_script import Manager, Shell,Server
from flask_migrate import Migrate, MigrateCommand

from asset import models

app = create_app('development')
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
server = Server(host="0.0.0.0",port=5000)
manager.add_command("runserver", server)
@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: # `Dict`
    """
    #     pass
    return dict(app=app,
                db=models.db,
                IDC=models.IDC,
                Asset=models.Asset,
                Manufactory=models.Manufactory,
                BusinessUnit=models.BusinessUnit
                )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run(default_command="runserver")
