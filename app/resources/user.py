#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from app.models.user import UserModel
from app.util.encoder import AlchemyEncoder
import json
from app.util.logz import create_logger


class User(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = User.parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return {'message': 'Wrong username or password.'}, 401
        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(
            identity=json.dumps(user, cls=AlchemyEncoder))
        return jsonify(access_token=access_token)

    @jwt_required()  # Requires dat token
    def get(self):
        # We can now access our sqlalchemy User object via `current_user`.
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )


class UserRegister(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('username', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'UserModel has already been created, aborting.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'user has been created successfully.'}, 201
