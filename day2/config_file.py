
class Config():
    DEBUG = False

class localDevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    
    SECRET_KEY = 'Shhhhhhh.....its a secret'
    SECURITY_TRACKEABLE = True


class deloyConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'