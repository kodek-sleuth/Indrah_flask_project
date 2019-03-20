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