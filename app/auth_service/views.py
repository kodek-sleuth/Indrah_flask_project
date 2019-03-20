from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from Models.models import User, BlackListToken
from flasgger import swag_from

def get_authenticated_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        access_token = auth_header
    except (IndexError, ValueError):
        return 'Authorization header is in wrong format.'
    if not access_token:
        return None
    else:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id, str):
            # user is authenticated so get the user
            user = User.query.get(user_id)
            return user
        elif user_id == 'You are already logged out':
            return user_id
        else:
            return None


#  class to register new user
class RegistrationView(MethodView):
    """document api"""
    @swag_from('swagger_docs/register_user.yaml', methods=['POST'])
    def post(self):
        # Handle POST request for this view. Url ---> /auth/register"""
        # Query to see if the user already exists
        post_data = request.get_json()
        username = post_data['username']
        password = post_data['password']
           
        # Register new user
        if username== True:
            return make_response(jsonify({"message": "username cannot be a numeric value"}))
    
        else:
            User.save_user(username, password)
            response = {
                'message': 'User registered successfully.'
            }

            # return user registered successfully message
            return make_response(jsonify(response)), 201


# class to handle user login and token generation
class LoginView(MethodView):
    @swag_from('swagger_docs/login.yaml', methods=['POST'])
    def post(self):
        # Handle POST request for this view. Url ---> /auth/login
        try:
            post_data = request.get_json(force=True)
            
            # Get the user object using their username (unique to every user)
            if "username" not in post_data.keys():
                return make_response(jsonify({"message": "json body must contain username key"})), 500
            
            if len(post_data.keys()) > 2:
                return make_response(jsonify({"message": "too many arguments in json body"})), 500
            
            user = User.query.filter_by(username=post_data['username']).first()
            # Try to authenticate the found user using their password
            if user and user.validate_password(post_data['password']):
               
		 # Generate the access token. This will be used as the authorization header
                user_access_token = user.user_generate_token(user.id)
                if user_access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': user_access_token.decode('utf-8')
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid username or password'
                }
                return make_response(jsonify(response)), 401

        except Exception as ex:
            # Create a response containing an string error message
            response = {
                'message': str(ex)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

#Define the API resources
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])

# Define the rule for the login url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
