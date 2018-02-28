# manage.py

import os
from flask_script import Manager, Shell 
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

"""define command for testing called test"""
@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()