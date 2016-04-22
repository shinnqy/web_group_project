#!/usr/bin/env python
import os
from app import create_app
from app.models import User
from flask.ext.script import Manager, Shell
# from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# migrate = Migrate(app, db)
 
def make_shell_context():
	return dict(app = app, User = User)

manager.add_command("shell", Shell(make_context = make_shell_context))

# @manager.command
# def deploy():
#     """Run deployment tasks."""
#     # from flask.ext.migrate import upgrade
#     from app.models import Role, User

#     # create user roles
#     Role.insert_roles()

#     # create self-follows for all users
#     User.add_self_follows()

if __name__ == '__main__':
	manager.run()