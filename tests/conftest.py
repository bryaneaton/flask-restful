#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test configuration and fixtures."""

import os
import pytest
from flask_jwt_extended import create_access_token

# Set test database URL before importing app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    from app.app import app as flask_app
    from app.db import db as _db

    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_SECRET_KEY': 'test-secret-key',
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """Provide database for testing."""
    from app.db import db as _db
    return _db


@pytest.fixture(scope='function')
def auth_headers(app):
    """Create JWT token for authenticated requests."""
    from app.db import db as _db
    from app.models.user import UserModel
    from app.util.encoder import AlchemyEncoder
    import json

    with app.app_context():
        # Create a test user
        user = UserModel(username='testuser', password='testpass')
        _db.session.add(user)
        _db.session.commit()

        # Create access token
        access_token = create_access_token(
            identity=json.dumps(user, cls=AlchemyEncoder)
        )

        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }


@pytest.fixture(scope='function')
def sample_user(db):
    """Create a sample user for testing."""
    from app.models.user import UserModel

    user = UserModel(username='sampleuser', password='samplepass')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def sample_store(db):
    """Create a sample store for testing."""
    from app.models.store import StoreModel

    store = StoreModel(name='Test Store')
    db.session.add(store)
    db.session.commit()
    return store


@pytest.fixture(scope='function')
def sample_item(db, sample_store):
    """Create a sample item for testing."""
    from app.models.item import ItemModel

    item = ItemModel(name='Test Item', price=19.99, store_id=sample_store.id)
    db.session.add(item)
    db.session.commit()
    return item
