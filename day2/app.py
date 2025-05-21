from flask import Flask, request
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


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    if not password:
        return {"error": "Password is required"}, 400
    
    if not email and not username:
        return {"error": "Email and username is required"}, 400
    
    if user_datastore.find_user(email=email) or user_datastore.find_user(username=username):
        return {"error": "User already exists"}, 400
    
    user_datastore.create_user(email=email, password=password, username=username, roles=["user"])
    db.session.commit()

    return {"message": "User registered successfully"}, 201


if __name__ == '__main__':
    app.run()