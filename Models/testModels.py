
from flask import current_app
from app import *

class User(db.Model):
    """
    class User that represents the user database model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(500))

    def __init__(self, username, password):
        self. username =  username
        self.password = password

    
    def addUser(_username, _password):
        addedUser = User(username=_username, password=_password)
        db.session.add(addedUser)
        db.session.commit()
    
    def __repr__(self):
        userObject = {
            "Username":self.username,
            "Password":self.password
        }
        
        return json.dumps(userObject)