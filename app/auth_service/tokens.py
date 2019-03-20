#This file shows how the token is fetched
#The function below means that jwt_required function checks for a token in query string or headers and verifies it 
#Further proving the function jwt.docode


from app import *
from functools import wraps
from flask import current_app

def jwt_required(U):
    @wraps(U)
    def wrapper(*args, **kwargs):
        token=request.args.get('token')
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'])
            return U(*args, **kwargs)
        
        except:
            return jsonify({"AUTH ERROR": "USER AUTHORISATION REQUIRED"})
    
    return wrapper