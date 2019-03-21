import json
import sys
from flask import make_response


class Response(object):
    def __init__(self, Success, Data=None, Message=None, Error=None, Response_code=200):
        self.Success = Success
        self.Data = Data
        self.Message = Message
        self.Error = Error
        self.Response_code = Response_code

    def to_dict(self):
        return{
            "Success": self.Success,
            "Data": self.Data,
            "Message": self.Message,
            "Error": self.Error
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def flask_response(self):
        return make_response(self.to_json(), self.Response_code)
