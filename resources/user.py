import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'UserModel has already been created, aborting.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Insert into users values (NULL,?,?)"

        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': '{} has been created successfully.'.format(data['username'])}, 201
