#I used class Based views for this routes but even normal functions work
#We Using swag_from to fetch the yaml file for that route and assigning it a method


import jwt
from app.auth_service import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from Models.models import *
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
                    data={
                        "Message":"An account already exists with that Username"
                    }
                    return make_response(jsonify(data)), 409

            except:
                if '~!@#$%&*():;+=-/' in username:
                    response={
                        "Message":"Username can only have Letters and numbers at the end"
                    }
                    
                    return make_response(jsonify(response)), 401

                else:
                    userReg=User.addUser(username, password)
                    data={
                        "Message":"You have successfully Created a User account"
                    }
                    return make_response(jsonify(data)), 201
    
        except:
            data={
                "Message":"Please Enter valid Credentials"
            }
            return make_response(jsonify(data)), 409


# class to handle user login and token generation
class LoginView(MethodView):
    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        request_data = request.get_json(force=True)
        
        user=User.query.filter_by(Username=request_data["Username"]).first()
        
        if user.Username==request_data["Username"] and user.Password==request_data["Password"]:
            
            expiration_time=datetime.datetime.utcnow()+datetime.timedelta(hours=1)
            
            #Creating The JWT token to be Returned
            token=jwt.encode({'exp':expiration_time}, current_app.config['SECRET_KEY'], algorithm='HS256')
            

            #Returning A success Message and The Token
            data={
                "Message":"You have successfully Logged In",
                "Access_Token": token.decode('utf-8')
            }
            
            return make_response(jsonify(data)), 201
        
        elif user.password!=request_data["password"]:
            data={
                "Message":"Invalid Password"
            }
            return make_response(jsonify(data)), 401


#The Protected Route To test if The JWT token Works also documented
#The Use of the decorators array is the same as using @jwt_required
class Protected(MethodView):
    decorators=[jwt_required]
    
    @swag_from('swagger_docs/protected.yaml', methods=['GET'])
    def get(self):
        data={
            "Message": "Only Protected"
        }
        return make_response(jsonify(data)), 200

#Turning Our Classes to Functions
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
protected  = Protected.as_view('protected')

#Adding the routes 'The add_url_rule' is the same as @route 
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth_blueprint.add_url_rule('/protected', view_func=protected, methods=['GET'])
