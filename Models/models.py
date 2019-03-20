import jwt
import os
from flask import current_app
from app import *
from datetime import datetime, timedelta
import unicodedata


class User(db.Model):
    """
    class User that represents the user database model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(500))
   

    def __init__(self, username, password=''):
        self.username = username
        self.password = password

    @staticmethod
    def get_all_users():
        """
        Static function to return all users in the database
        """
        return User.query.all()

    def save(self):
        """save function that commits user instance to be saved to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """delete user from database
        """
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def is_number(username):
        """function to check if provided string is an integer
        """
        try:
            float(username)
            return True
        except ValueError:
            pass

        try:
            unicodedata.numeric(username)
            return True
        except (TypeError, ValueError):
            return False

    def user_generate_token(self, userid):
        """Generate token for user
        """
        try:
            # set up a payload with an expiration date
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=(60 * 60 * 60)),
                'iat': datetime.utcnow(),
                'sub': userid
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as ex:
            return str(ex)

    @staticmethod
    def decode_token(token):
        """Function to decode the token
        """
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            is_blacklisted_token = BlackListToken.check_blacklist(
                auth_token=token)
            if is_blacklisted_token:
                return 'Token Blacklisted. Please log in'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            # if the token is expired, return an error string
            return "The token is expired. Login to renew token"
        except jwt.InvalidTokenError:
            # if the token is invalid, return an error string
            return "Invalid token. Login or Register"

    def __repr__(self):
        return "<User: {}>".format(self.username)


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
