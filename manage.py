from flask_script import Manager, Server
from application import app

manager = Manager(app)

manager.add_command('runserver', Server(host='127.0.0.1', port=9999))


if __name__ == '__main__':
    # manager.run()
    app.run(host='127.0.0.1', port=9999, debug=True)
