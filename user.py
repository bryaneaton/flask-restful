import sqlite3
from flask_restful import Resource, reqparse


class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select id, username, password from users where username = ?"
        result = cursor.execute(query, (username,))  # parameters must be in form of tuple
        row = result.fetchone()

        if row:
            user = cls(*row)  # cls is the User Class, i.e. using a class method
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select id, username, password from users where id = ?"
        result = cursor.execute(query, (_id,))  # parameters must be in form of tuple
        row = result.fetchone()

        if row:
            user = cls(*row)  # cls is the User Class, i.e. using a class method
        else:
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User has already been created, aborting.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Insert into users values (NULL,?,?)"

        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User has been created successfully.'}, 201
