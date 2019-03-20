
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
