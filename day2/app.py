from flask import Flask
from flask_security import Security

from models import db, user_datastore


def create_app():

    init_app = Flask(__name__)

    from config_file import localDevConfig
    init_app.config.from_object(localDevConfig)

    db.init_app(init_app)

    Security(init_app, user_datastore)
    return init_app

app = create_app()

@app.route('/')
def index():
    return {"message": "Hello, World!"}



if __name__ == '__main__':
    app.run()