from flask import request
from flask_restful import Resource
from Model import db, Accounts, AccountSchema

accounts_schema = AccountSchema(many=True)
account_schema = AccountSchema()

class RegisterResource(Resource):
    def get(self):
        accounts = Accounts.query.all()
        accounts = accounts_schema.dump(accounts).data
        return {'message': 'success'}, 201

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        #data, errors = account_schema.load(json_data)
        data = account_schema.load(json_data)
#         if errors:
#             return errors, 422
        account = Accounts.query.filter_by(email=data['email']).first()
        if account:
            return {'message': 'Email already in use!'}, 401
        account = Accounts(
            email=json_data['email'],
            password=json_data['password']
            )

        db.session.add(account)
        db.session.commit()

        #result = account_schema.dump(account).data

        return { 'message': 'Successfully Registered !'}, 200
