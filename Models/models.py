import json
from app import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(15), nullable=False, unique=True)
    Password = db.Column(db.String(200), nullable=False)

  
    def __init__(self, Username, Password):
        self.Username = Username
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


