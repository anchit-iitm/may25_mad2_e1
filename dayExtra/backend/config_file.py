
class Config():
    DEBUG = False

class localDevConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    
    SECRET_KEY = 'Shhhhhhh.....its a secret'
    SECURITY_TRACKEABLE = True
    SECURITY_LOGIN_URL = '/ami_chaina'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 2
    CACHE_KEY_PREFIX = 'dayExtra_'
    CACHE_DEFAULT_TIMEOUT = 60 #in seconds

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'donot_reply@x.com'


class deloyConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


class celeryConfig():
    broker_url = 'redis://localhost:6379/3'
    result_backend = 'redis://localhost:6379/4'
    timezone = 'Asia/Kolkata'