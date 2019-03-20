import sqlite3
import os
class Config():
    USER_SECRET_KEY='its nolonger a secret'
    ADMIN_SECRET_KEY='secret'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
    SQLALCHEMY_DATABASE_URI='postgresql://josekodek:kevina52@localhost:5432/foodhub'

class DevelopmentConfig(Config):
    DEBUG=True
    DEVELOPMENT=True
    USER_SECRET_KEY='its nolonger a secret'
    ADMIN_SECRET_KEY='secret'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
    
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG=True
    TESTING=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    USER_SECRET_KEY='i wont tell if you dont'
    ADMIN_SECRET_KEY='secret'
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'


 

app_config={
    'development': DevelopmentConfig,
    'testing': TestingConfig
}