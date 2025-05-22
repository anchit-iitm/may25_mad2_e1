from models import db, user_datastore
# from app import app
# from flask import current_app as app
from app import create_app

app, _ = create_app()

def register_admin():
    if not user_datastore.find_user(email="admin@abc.com") and user_datastore.find_role("admin"):
        user_datastore.create_user(email="admin@abc.com", password="admin", username="admin", roles=["admin", "user"])
        '''
        new_data = User(email="admin@abc.com", password="admin", username="admin")

        db.session.add(new_data)
        '''
        db.session.commit()

def create_roles():
    user_datastore.find_or_create_role(name="admin")
    '''
    Role(name="admin")
    db.session.add(new_data)
    '''
    user_datastore.find_or_create_role(name="user")
    db.session.commit()
    return True

with app.app_context():
    db.create_all()

    create_roles()
    register_admin()

