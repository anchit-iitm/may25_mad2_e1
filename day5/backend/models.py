from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, RoleMixin, UserMixin

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) #

    email = db.Column(db.String(255), unique=True) #
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False) #

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    active = db.Column(db.Boolean()) #
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False) #

    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)

    def get_all():
        all_data = Category.query.all()
        if not all_data:
            return False
        return [
            {
                "id": data.id,
                "name": data.name,
                "description": data.description,
                "status": data.deleted
            }
            for data in all_data
        ]
    
    def get_by_id(id):
        data = Category.query.filter_by(id=id).first()
        if not data:
            return False
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description
        }
    
    def create(name, description):
        if Category.query.filter_by(name=name).first():
            return False
        data = Category(name=name, description=description)
        db.session.add(data)
        db.session.commit()
        return True
    
    def update(id, name, description):
        data = Category.query.filter_by(id=id).first()
        if not data:
            return False
        data.name = name if name else data.name
        data.description = description if description else data.description
        db.session.commit()
        return True
    
    def delete(id):
        data = Category.query.filter_by(id=id).first()
        if not data:
            return 1
        # Soft delete
        if data.deleted == True:
            data.deleted = False
            db.session.commit()
            return 2
        elif data.deleted == False:
            data.deleted = True
            db.session.commit()
            return 3
    

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))