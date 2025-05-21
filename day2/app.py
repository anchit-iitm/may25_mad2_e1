from flask import Flask, request
from flask_security import Security, auth_required, roles_accepted

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


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email and not username:
        return {"error": "Email or username is required"}, 400

    if not password:
        return {"error": "Password is required"}, 400

    user = user_datastore.find_user(email=email) if email else user_datastore.find_user(username=username)
    if not user:
        return {"error": "User not found, register with us"}, 404

    if user.password != password:
        return {"error": "Invalid password"}, 401
    
    if not user.is_active:
        return {"error": "User is inactive, contact admin"}, 403

    return {
        "message": "Login successful",
        "authToken": user.get_auth_token(),
        "user": {"email": user.email, "username": user.username, "roles": [role.name for role in user.roles]}
        }, 200


@app.route('/test', methods=['POST'])
@auth_required('token')
@roles_accepted('admin')
def test():
    return {"message": "Test route running successfully"}

@app.route('/category/get/all', methods=['GET'])
@auth_required('token')
def get_all_category():
    from models import Category
    data = Category.get_all()
    return {
        "categories": data if data else "No categories found"
    }, 200




if __name__ == '__main__':
    app.run()