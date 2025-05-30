from app import celery_app
from celery_context import ContextTask



@celery_app.task(base=ContextTask)
def hello_world():
    print("Hello, World!")
    return "Hello, World!"

@celery_app.task(base=ContextTask)
def add(x, y):
    from time import sleep
    sleep(5)
    print(f"Adding {x} and {y}")
    return x + y

@celery_app.task(base=ContextTask)
def query_db():
    from models import User
    users = User.query.all()
    print(f"Queried {len(users)} users from the database.")
    return [user.username for user in users] if users else []