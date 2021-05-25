from flask import request, session
from flask_restful import Resource
from Model import db, Accounts, AccountSchema
import json

#categories_schema = CategorySchema(many=True)
account_schema = AccountSchema()

class LoginResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(type(json_data))
        print(json_data)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        #data, errors = account_schema.load(json_data)
        data = account_schema.load(json_data)
        print(type(data))
        print(data)
#         if errors:
#             return errors, 400
        account = Accounts.query.filter_by(email = data['email'], password = data["password"]).first()
        if account:
            session['loggedin'] = True
            session['email'] = account.email
            msg = 'Logged in successfully !'
            return {'message': msg}, 200
        else:
            msg = 'Incorrect username / password !'
            return {'message': msg}, 401
