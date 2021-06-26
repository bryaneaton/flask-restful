#!/usr/bin/env python3

from werkzeug.security import safe_str_cmp

from app.models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    ## TODO: don't use plain text passwords
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
