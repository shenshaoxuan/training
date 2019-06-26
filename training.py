from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from app.model.user import User
from app.model.course import Course


app = create_app()

manager = Manager(app)
manager.add_command("db", MigrateCommand)




if __name__ == '__main__':
    # app.__call__
    manager.run()
