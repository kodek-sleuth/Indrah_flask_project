import sqlite3
import os
class Config():
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 

class DevelopmentConfig(Config):
    DEBUG=True
    DEVELOPMENT=True
    SECRET_KEY='its nolonger a secret'
    SQLALCHEMY_DATABASE_URI='sqlite:///develope.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False 
    
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG=True
    TESTING=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='i wont tell if you dont'
    SQLALCHEMY_DATABASE_URI='sqlite:///testing.db'


app_config={
    'development': DevelopmentConfig,
    'testing': TestingConfig
}