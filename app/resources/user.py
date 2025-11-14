#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from app.models.user import UserModel
from app.util.encoder import AlchemyEncoder
import json
from app.util.logz import create_logger

user_bp = Blueprint('user', __name__)
logger = create_logger()


@user_bp.route('/user', methods=['POST'])
def login():
    """User login endpoint."""
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate required fields
    if 'username' not in data:
        return jsonify({'message': 'username field cannot be left blank'}), 400
    if 'password' not in data:
        return jsonify({'message': 'password field cannot be left blank'}), 400

    username = data['username']
    password = data['password']

    user = UserModel.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Wrong username or password.'}), 401
    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(
        identity=json.dumps(user, cls=AlchemyEncoder))
    return jsonify(access_token=access_token)


@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information."""
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        username=current_user.username,
    )


@user_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint."""
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate required fields
    if 'username' not in data:
        return jsonify({'message': 'username field cannot be left blank'}), 400
    if 'password' not in data:
        return jsonify({'message': 'password field cannot be left blank'}), 400

    if UserModel.find_by_username(data['username']):
        return jsonify({'message': 'UserModel has already been created, aborting.'}), 400

    user = UserModel(**data)
    user.save_to_db()

    return jsonify({'message': 'user has been created successfully.'}), 201
