#Ceating The User Model

from flask import current_app
from app import *

class User(db.Model):
    """
    class User that represents the user database model
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(20), unique=True)
    Password = db.Column(db.String(500))

    def __init__(self, Username, Password):
        self.Username =  Username
        self.Password = Password

    
    def addUser(_Username, _Password):
        addedUser = User(Username=_Username, Password=_Password)
        db.session.add(addedUser)
        db.session.commit()
    
    def __repr__(self):
        userObject = {
            "Username":self.Username,
            "Password":self.Password
        }
        
        return json.dumps(userObject)
