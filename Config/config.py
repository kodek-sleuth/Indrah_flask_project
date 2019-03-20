import sqlite3

class Config():
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
   

class DevelopmentConfig(Config):
    DEBUG=True
    DEVELOPMENT=True
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

app_config={
    'development': DevelopmentConfig
}