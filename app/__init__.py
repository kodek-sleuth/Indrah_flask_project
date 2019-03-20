import jwt
import datetime
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from Settings.config import app_config
from flask import Flask, request, jsonify, make_response, redirect

db = SQLAlchemy()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SWAGGER'] = {
        'swagger': '2.0',
        'title': 'Just  A simple App',
        'description': "Just  A simple App. This is a RESTful API built in python using the Flask Framework.\
        \nGitHub Repository: 'https://github.com/kodek-sleuth/Indrah_flask_project'",
        'basePath': '/',
        'version': '0.1.0',
        'contact': {
            'Developer': 'Kodek-Sleuth'
        },

        'schemes': [
            'https'
        ],

        'tags': [
            {
                'name': 'User',
                'description': 'The basic unit of authentication'
            },
        ],

        'specs_route': '/swagger_docs/'
    }

    
    db.init_app(app)
    swagger=Swagger(app)

    @app.route('/')
    def index():
        return redirect('/swagger_docs/')

    from .auth_service import auth_blueprint    
    app.register_blueprint(auth_blueprint)

    return app
