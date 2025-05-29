from flask import Flask, request
from flask_security import Security, auth_required, roles_accepted
from flask_restful import Api
from flask_cors import CORS
from models import db, user_datastore

def create_app():

    init_app = Flask(__name__)

    from config_file import localDevConfig
    init_app.config.from_object(localDevConfig)

    db.init_app(init_app)

    Security(init_app, user_datastore)

    init_api = Api(init_app, prefix='/api')

    CORS(init_app)

    return init_app, init_api

app, api = create_app()

from routes.category import getCategory, updateCategory
api.add_resource(getCategory, '/category') #localhost:5000/api/category
api.add_resource(updateCategory, '/category/update')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        return {"message": f"Received data: {data}"}, 200
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
    userid = data.get('email')
    password = data.get('password')
    print(userid, password)
    if not userid:
        return {"message": "Email or username is required"}, 400

    if not password:
        return {"message": "Password is required"}, 400

    user = user_datastore.find_user(email=userid)
    if not user:
        if user_datastore.find_user(username=userid):
            print(user.username)
            user = user_datastore.find_user(username=userid)
        
        return {"message": "User not found, register with us"}, 404

    if user.password != password:
        return {"message": "Invalid password"}, 401
    
    if not user.is_active:
        return {"message": "User is inactive, contact admin"}, 403

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

@app.route('/category', methods=['PATCH', 'POST']) #localhost:5000/category
@auth_required('token')
def get_category():
    if request.method == 'POST':
        from models import Category
        data = Category.get_all()
        if not data:
            return {
                "error": "No categories found"
            }, 404
        return {
            "categories": data
        }, 200
    
    if request.method == 'PATCH':
        id = int(request.json.get('id'))
        print(type(id))
        if not id:
            return {
                "error": "ID is required"
            }, 400
        from models import Category
        data = Category.get_by_id(id)
        if not data:
            return {
                "error": "Category not found"
            }, 404
        return {
            "category": data
        }, 200  

@app.route('/category/update', methods=['PUT', 'PATCH', 'POST'])
@auth_required('token')
@roles_accepted('admin')
def update_category():
    from models import Category
    data = request.json
    if request.method == 'POST':
        if Category.create(data.get('name'), data.get('description')):
            return {
                "message": "Category created successfully"
            }, 201
        else:
            return {
                "error": "Category already exists"
            }, 400

    if request.method == 'PUT':
        id = data.get('id')
        if Category.update(id, data.get('name'), data.get('description')):
            return {
                "message": "Category updated successfully"
            }, 200
        else:
            return {
                "error": "Category not found"
            }, 404

    elif request.method == 'PATCH':
        if not data.get('id'):
            return {
                "error": "ID is required"
            }, 400
        if Category.delete(data.get('id')) == 3:
            return {
                "message": "Category deleted successfully"
            }, 201
        elif Category.delete(data.get('id')) == 2:
            return {
                "message": "Category restored successfully"
            }, 201
        else:
            return {
                "error": "Category not found"
            }, 404


if __name__ == '__main__':
    app.run()