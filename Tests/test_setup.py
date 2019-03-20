#This file Houses the Setup which is going to occur each Time the Tests code is run

import json
import unittest
from app import create_app, db

class AuthTest(unittest.TestCase):
    def setUp(self):
        
        #We using the testing Config/Instance
        self.app = create_app(config_name='testing')
        
        #This self.client is going to make all the Requests
        self.client = self.app.test_client
        
        #Whatever code is below is the code which is going to be executed when the app is running
        with self.app.app_context():
            self.userRegDetails = {
                "Username":"userTest",
                "Password":"usertest"
            }

            self.userLogDetails = {
                "Username":"userTest",
                "Password":"usertest"
            }

            db.session.close()
            db.drop_all()
            db.create_all()
class BlackListToken(db.Model):
    """Class to blacklist expired tokens
    """
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(
        db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def save(self):
        """function to save expired token
        """
        db.session.add(self)
        db.session.commit()

    def check_blacklist(auth_token):
        """function to check if token is blacklisted
        """
        # check whether token has been blacklisted
        res = BlackListToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
 
#For every time We Run the python3 -m pytest The database will be created and deleted and then created for the next test
            