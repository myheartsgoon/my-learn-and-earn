from flask_script import Manager, Server
from application import create_app
from flask_migrate import Migrate, MigrateCommand
from application import db

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('runserver', Server(host='0.0.0.0', port=8080))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0', port=8080)
