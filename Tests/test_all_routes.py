import json
import test_setup

class User_Resgister_Login_TestCase(test_setup.AuthTest):
    
    #Testing if a user Can Register
    def test_Register_route(self):
        res=self.client().post('/auth/register', data=json.dumps(self.userRegDetails), content_type='application/json')
        result=json.loads(res.data.decode())
        self.assertEqual(result["Message"], "You have successfully Created a User account")
        self.assertEqual(res.status, '201 CREATED')
    
    #Testing If a user can Login
    def test_Login_route(self):
        #Making That a user that Registers successfully gets Logged in and gets Token
        request_Reg=self.client().post('/auth/register', data=json.dumps(self.userRegDetails), content_type='application/json')
        result=json.loads(request_Reg.data.decode())
        self.assertEqual(result["Message"], "You have successfully Created a User account")
        self.assertEqual(request_Reg.status, '201 CREATED')

        #Making sure that user gets Logged In and Recieves Token
        request_Log=self.client().post('/auth/login', data=json.dumps(self.userLogDetails), content_type='application/json')
        result=json.loads(request_Log.data.decode())
        self.assertEqual(result["Message"], "You have successfully Logged In")
        self.assertEqual(result["Access_Token"], result["Access_Token"])
        self.assertEqual(request_Log.status, '201 CREATED')
    
    def test_protected(self):
        #Registering A User
        res=self.client().post('/auth/register', data=json.dumps(self.userRegDetails), content_type='application/json')
        result=json.loads(res.data.decode())
        self.assertEqual(result["Message"], "You have successfully Created a User account")
        self.assertEqual(res.status, '201 CREATED')
    

       #Making sure that user gets Logged In and Recieves Token
        request_Log=self.client().post('/auth/login', data=json.dumps(self.userLogDetails), content_type='application/json')
        result=json.loads(request_Log.data.decode())
        self.assertEqual(result["Message"], "You have successfully Logged In")
        self.assertEqual(result["Access_Token"], result["Access_Token"])
        self.assertEqual(request_Log.status, '201 CREATED')
    

        #Making sure that user gets Logged In and Recieves Token
        request_Log=self.client().get('/protected?token='+ result['Access_Token'])
        result=json.loads(request_Log.data.decode())
        self.assertEqual(result["Message"], "Only Protected")
        self.assertEqual(request_Log.status, '200 OK')
    
        #Making Sure A User requires a Token to use the Protected Route

