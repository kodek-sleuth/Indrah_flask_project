#This file is going to house our Main app and the App_Context
#The App Context enables Us to determine which type of our app We should Run
#I created Two app instances in The Config file one For Development and One for Testing
#So On line 11 we want to use the instance of development
#Then we going to create all tables
#Its in this file where we import the create_app 

from app import create_app
from Models.models import *

app = create_app('development')

with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True, port=3000)