#I used class Based views for this routes but even normal functions work
#We Using swag_from to fetch the yaml file for that route and assigning it a method


import jwt
from app.auth_service import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from Models.models import *
from Models.Response import Response
from flasgger import swag_from
from app.auth_service.tokens import jwt_required

class RegistrationView(MethodView):
    @swag_from('swagger_docs/register_user.yaml', methods=['POST'])
    def post(self):
        try:
            #To fetch The Json entered on this Route
            request_data = request.get_json(force=True)
            
            #Assigning the values entered to these Variables
            username=request_data["Username"]
            password=request_data["Password"]
            try:

                #Checking if User exists in db, if so then...
                user=User.query.filter(Username=username).first()
                if user.Username==username:
                    response = Response(Success=False, Error="An account already exists with that Username", response_code=401)
                    return response.flask_response()

            except:
                if '~!@#$%&*():;+=-/' in username:    
                    response = Response(Success=False, Error="Username can only have Letters and numbers at the end", response_code=401)
                    return response.flask_response()

                else:
                    userReg=User.addUser(username, password)
                    data={
                        "Message":"You have Successfully Created a User account"
                    }

                    response = Response(Success=True, Message="OK", Data=data)
                    return response.flask_response()
    
        except:
            response = Response(Success=False, Error="Invalid Credentials", Response_code=401)
            return response.flask_response()


# class to handle user login and token generation
class LoginView(MethodView):
    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        try:
            request_data = request.get_json(force=True)
            
            user=User.query.filter_by(Username=request_data["Username"]).first()
            
            if user.Username==request_data["Username"] and user.Password==request_data["Password"]:
                
                expiration_time=datetime.datetime.utcnow()+datetime.timedelta(hours=1)
                
                #Creating The JWT token to be Returned
                token=jwt.encode({'exp':expiration_time}, current_app.config['SECRET_KEY'], algorithm='HS256')
            
                #Returning A Success Message and The Token
                data={
                    "Message":"You have Successfully Logged In",
                    "Access_Token": token.decode('utf-8')
                }

                response = Response(Success=True, Message="OK", Data=data)
                return response.flask_response()
            
            elif user.Password!=request_data["Password"]:    
                response = Response(Success=False, Error="Invalid Password", Response_code=401)
                return response.flask_response()
        
        except:
            response = Response(Success=False, Error="Invalid Password or Username", Response_code=401)
            return response.flask_response()



#The Protected Route To test if The JWT token Works also documented
#The Use of the decorators array is the same as using @jwt_required
class Protected(MethodView):
    decorators=[jwt_required]
    
    @swag_from('swagger_docs/protected.yaml', methods=['GET'])
    def get(self):
        data={
            "Message": "Only Protected"
        }
        
        response = Response(Success=True, Message="OK", Data=data)    
        return response.flask_response()

#Turning Our Classes to Functions
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
protected  = Protected.as_view('protected')

#Adding the routes 'The add_url_rule' is the same as @route 
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/protected', view_func=protected, methods=['GET'])
