import json
import unittest
from app import create_app, db

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        with self.app.app_context():
            self.userRegDetails = {
                "Username":"userTest",
                "Password":"usertest"
            }

            self.userLogDetails = {
                "Username":"userTest",
                "Password":"usertest"
            }

            db.session.close()
            db.drop_all()
            db.create_all()

            