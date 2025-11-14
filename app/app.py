#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask
from flask_jwt_extended import JWTManager

from app.resources.item import item_bp
from app.resources.store import store_bp
from app.resources.user import user_bp
from app.config import postgresqlConfig

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "Dese.Decent.Pups.BOOYO0OST"  # Change this!
jwt = JWTManager(app)

# Initialize database
from app.db import db
db.init_app(app)


# JWT user loader callback
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Load user from JWT token identity."""
    import json
    from app.models.user import UserModel

    identity = jwt_data["sub"]
    try:
        user_data = json.loads(identity)
        return UserModel.find_by_id(user_data.get('id'))
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


# Register blueprints
app.register_blueprint(item_bp)
app.register_blueprint(store_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    # Create database tables when running directly
    with app.app_context():
        db.create_all()
    # TODO: Add swagger integration
    app.run(debug=True)  # important to mention debug=True
