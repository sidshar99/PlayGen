from flask import request, session
from flask_restful import Resource

class LogoutResource(Resource):
    def get(self):
        session.pop('loggedin', None)
        session.pop('email', None)

        msg = 'Logged out successfully !'
        return {'message': msg}, 200
