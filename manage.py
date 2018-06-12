from flask_script import Manager, Server
from application import app

manager = Manager(app)

manager.add_command('runserver', Server(host='0.0.0.0', port=8080))


if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0', port=8080, debug=True)
