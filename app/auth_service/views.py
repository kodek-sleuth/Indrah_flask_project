import jwt
from app.auth_service import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from Models.models import *
from flasgger import swag_from
from app.auth_service.tokens import jwt_required

#  class to register new user
#Creating Class based views for Registration, Login and Logout as well as The Token
class RegistrationView(MethodView):
    @swag_from('swagger_docs/register_user.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            username=request_data["Username"]
            password=request_data["Password"]
            try:
                user=User.query.filter(Username=username).first()
                if user.Username==username:
                    response={
                        "Message":"An account already exists with that Username"
                    }
                    return make_response(jsonify(response)), 409

            except:
                if '~!@#$%&*():;+=-/' in username:
                    response={
                        "Message":"Username can only have Letters and numbers at the end"
                    }
                    
                    return make_response(jsonify(response)), 401

                else:
                    userReg=User.addUser(username, password)
                    response={
                        "Message":"You have successfully Created a User account"
                    }
                    return make_response(jsonify(response)), 201
    
        except:
            response={
                "Message":"Please Enter valid Credentials"
            }
            return make_response(jsonify(response)), 409


# class to handle user login and token generation
class LoginView(MethodView):
    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        request_data = request.get_json(force=True)
        user=User.query.filter_by(Username=request_data["Username"]).first()
        if user.Username==request_data["Username"] and user.Password==request_data["Password"]:
            expiration_time=datetime.datetime.utcnow()+datetime.timedelta(hours=1)
            token=jwt.encode({'exp':expiration_time}, current_app.config['SECRET_KEY'], algorithm='HS256')
            response={
                "Message":"You have successfully Logged In",
                "Access_Token": token.decode('utf-8')
            }
            
            return make_response(jsonify(response)), 201
        
        elif user.password!=request_data["password"]:
            response={
                "Message":"Invalid Password"
            }
            return make_response(jsonify(response)), 401

class Protected(MethodView):
    decorators=[jwt_required]
    @swag_from('swagger_docs/protected.yaml', methods=['GET'])
    def get(self):
        response = {
            "Message": "Only Protected"
        }
        return make_response(jsonify(response)), 200

#Define the API resources
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
protected  = Protected.as_view('prtected')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])

# Define the rule for the login url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/protected', view_func=protected, methods=['GET'])
