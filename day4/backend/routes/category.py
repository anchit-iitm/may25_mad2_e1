from flask import request
from flask_security import auth_required, roles_accepted
from flask_restful import Resource

# @app.route('/category', methods=['GET', 'POST'])
# def get_category():
 

class getCategory(Resource):
    # if request.method == 'POST':
    @auth_required('token')
    def post(self):
        from models import Category
        data = Category.get_all()
        if not data:
            return {
                "error": "No categories found"
            }, 404
        return {
            "categories": data
        }, 200
    
    # if request.method == 'GET':
    @auth_required('token')
    def get(self):
        id = request.json.get('id')
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

from models import Category
# @app.route('/category/update', methods=['PUT', 'DELETE', 'POST'])
class updateCategory(Resource):
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        data = request.json                 
        if Category.create(data.get('name'), data.get('description')):
            return {
                "message": "Category created successfully"
            }, 201
        else:
            return {
                "error": "Category already exists"
            }, 400

    @auth_required('token')
    @roles_accepted('admin')
    def put(self):
        data = request.json                 
        id = data.get('id')
        if Category.update(id, data.get('name'), data.get('description')):
            return {
                "message": "Category updated successfully"
            }, 200
        else:
            return {
                "error": "Category not found"
            }, 404

    @auth_required('token')
    @roles_accepted('admin')
    def delete(self): # 1 not found, 2 restored, 3 deleted
        data = request.json
        print(Category.delete(data.get('id')))
        if Category.delete(data.get('id')) == 3:
            return {
                "message": "Category deleted successfully"
            }, 201
        elif Category.delete(data.get('id')) == 2:
            return {
                "message": "Category restored successfully"
            }, 201
        elif Category.delete(data.get('id')) == 1:
            return {
                "error": "Category not found"
            }, 404
        else:
            return {
                "error": "Some unwanted error occurred"
            }, 404

