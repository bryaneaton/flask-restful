#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for API resources/endpoints."""

import json
import pytest
from app.models.user import UserModel
from app.models.item import ItemModel
from app.models.store import StoreModel


class TestUserRegister:
    """Tests for UserRegister resource."""

    def test_register_user_success(self, client, db):
        """Test successful user registration."""
        response = client.post('/register',
            data=json.dumps({'username': 'newuser', 'password': 'newpass'}),
            content_type='application/json')

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'user has been created successfully.'

        # Verify user exists in database
        user = UserModel.find_by_username('newuser')
        assert user is not None

    def test_register_duplicate_user(self, client, db, sample_user):
        """Test registering duplicate username."""
        response = client.post('/register',
            data=json.dumps({'username': 'sampleuser', 'password': 'pass'}),
            content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already been created' in data['message']

    def test_register_missing_username(self, client):
        """Test registration with missing username."""
        response = client.post('/register',
            data=json.dumps({'password': 'pass'}),
            content_type='application/json')

        assert response.status_code == 400

    def test_register_missing_password(self, client):
        """Test registration with missing password."""
        response = client.post('/register',
            data=json.dumps({'username': 'user'}),
            content_type='application/json')

        assert response.status_code == 400


class TestUser:
    """Tests for User resource (login)."""

    def test_login_success(self, client, db, sample_user):
        """Test successful user login."""
        response = client.post('/user',
            data=json.dumps({'username': 'sampleuser', 'password': 'samplepass'}),
            content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert data['access_token'] is not None

    def test_login_wrong_password(self, client, db, sample_user):
        """Test login with wrong password."""
        response = client.post('/user',
            data=json.dumps({'username': 'sampleuser', 'password': 'wrongpass'}),
            content_type='application/json')

        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Wrong username or password' in data['message']

    def test_login_nonexistent_user(self, client, db):
        """Test login with non-existent user."""
        response = client.post('/user',
            data=json.dumps({'username': 'nobody', 'password': 'pass'}),
            content_type='application/json')

        assert response.status_code == 401

    def test_get_user_authenticated(self, client, db, auth_headers):
        """Test getting user info when authenticated."""
        response = client.get('/user', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'username' in data or 'id' in data

    def test_get_user_unauthenticated(self, client, db):
        """Test getting user info without authentication."""
        response = client.get('/user')

        assert response.status_code == 401


class TestStore:
    """Tests for Store resource."""

    def test_get_store_success(self, client, db, sample_store):
        """Test getting an existing store."""
        response = client.get(f'/store/{sample_store.name}')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == sample_store.name

    def test_get_store_not_found(self, client, db):
        """Test getting non-existent store."""
        response = client.get('/store/NonExistent')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['message']

    def test_create_store_success(self, client, db, auth_headers):
        """Test creating a new store."""
        response = client.post('/store/NewStore', headers=auth_headers)

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'NewStore'

        # Verify store exists in database
        store = StoreModel.find_by_name('NewStore')
        assert store is not None

    def test_create_store_duplicate(self, client, db, sample_store, auth_headers):
        """Test creating duplicate store."""
        response = client.post(f'/store/{sample_store.name}', headers=auth_headers)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['message']

    def test_create_store_unauthenticated(self, client, db):
        """Test creating store without authentication."""
        response = client.post('/store/NewStore')

        assert response.status_code == 401

    def test_delete_store_success(self, client, db, sample_store, auth_headers):
        """Test deleting a store."""
        store_name = sample_store.name
        response = client.delete(f'/store/{store_name}', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deleted' in data['message']

        # Verify store is deleted
        store = StoreModel.find_by_name(store_name)
        assert store is None

    def test_delete_store_unauthenticated(self, client, db, sample_store):
        """Test deleting store without authentication."""
        response = client.delete(f'/store/{sample_store.name}')

        assert response.status_code == 401


class TestStoreList:
    """Tests for StoreList resource."""

    def test_get_all_stores_empty(self, client, db):
        """Test getting all stores when none exist."""
        response = client.get('/stores')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'stores' in data
        assert data['stores'] == []

    def test_get_all_stores(self, client, db, sample_store):
        """Test getting all stores."""
        # Create additional stores
        store2 = StoreModel(name='Store 2')
        store2.save_to_db()

        response = client.get('/stores')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'stores' in data
        assert len(data['stores']) == 2
        store_names = [s['name'] for s in data['stores']]
        assert 'Test Store' in store_names
        assert 'Store 2' in store_names


class TestItem:
    """Tests for Item resource."""

    def test_get_item_success(self, client, db, sample_item, auth_headers):
        """Test getting an existing item."""
        response = client.get(f'/item/{sample_item.name}', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == sample_item.name
        assert data['price'] == sample_item.price

    def test_get_item_not_found(self, client, db, auth_headers):
        """Test getting non-existent item."""
        response = client.get('/item/NonExistent', headers=auth_headers)

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'not found' in data['message']

    def test_get_item_unauthenticated(self, client, db, sample_item):
        """Test getting item without authentication."""
        response = client.get(f'/item/{sample_item.name}')

        assert response.status_code == 401

    def test_create_item_success(self, client, db, sample_store, auth_headers):
        """Test creating a new item."""
        response = client.post('/item/NewItem',
            data=json.dumps({'price': 25.50, 'store_id': sample_store.id}),
            headers=auth_headers)

        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'NewItem'
        assert data['price'] == 25.50

        # Verify item exists in database
        item = ItemModel.find_by_name('NewItem')
        assert item is not None

    def test_create_item_duplicate(self, client, db, sample_item, auth_headers):
        """Test creating duplicate item."""
        response = client.post(f'/item/{sample_item.name}',
            data=json.dumps({'price': 10.00, 'store_id': 1}),
            headers=auth_headers)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data['message']

    def test_create_item_missing_price(self, client, db, sample_store, auth_headers):
        """Test creating item without price."""
        response = client.post('/item/NewItem',
            data=json.dumps({'store_id': sample_store.id}),
            headers=auth_headers)

        assert response.status_code == 400

    def test_create_item_unauthenticated(self, client, db):
        """Test creating item without authentication."""
        response = client.post('/item/NewItem',
            data=json.dumps({'price': 10.00, 'store_id': 1}),
            content_type='application/json')

        assert response.status_code == 401

    def test_update_item_existing(self, client, db, sample_item, auth_headers):
        """Test updating an existing item."""
        response = client.put(f'/item/{sample_item.name}',
            data=json.dumps({'price': 99.99, 'store_id': sample_item.store_id}),
            headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['price'] == 99.99

        # Verify update in database
        item = ItemModel.find_by_name(sample_item.name)
        assert item.price == 99.99

    def test_update_item_create_new(self, client, db, sample_store, auth_headers):
        """Test updating creates new item if doesn't exist."""
        response = client.put('/item/BrandNewItem',
            data=json.dumps({'price': 15.00, 'store_id': sample_store.id}),
            headers=auth_headers)

        assert response.status_code == 200

        # Verify item was created
        item = ItemModel.find_by_name('BrandNewItem')
        assert item is not None

    def test_update_item_unauthenticated(self, client, db, sample_item):
        """Test updating item without authentication."""
        response = client.put(f'/item/{sample_item.name}',
            data=json.dumps({'price': 99.99, 'store_id': 1}),
            content_type='application/json')

        assert response.status_code == 401

    def test_delete_item_success(self, client, db, sample_item, auth_headers):
        """Test deleting an item."""
        item_name = sample_item.name
        response = client.delete(f'/item/{item_name}', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'deleted' in data['message']

        # Verify item is deleted
        item = ItemModel.find_by_name(item_name)
        assert item is None

    def test_delete_item_not_found(self, client, db, auth_headers):
        """Test deleting non-existent item."""
        response = client.delete('/item/NonExistent', headers=auth_headers)

        # Should still return 200 as per current implementation
        assert response.status_code == 200

    def test_delete_item_unauthenticated(self, client, db, sample_item):
        """Test deleting item without authentication."""
        response = client.delete(f'/item/{sample_item.name}')

        assert response.status_code == 401


class TestItemList:
    """Tests for ItemList resource."""

    def test_get_all_items_empty(self, client, db, auth_headers):
        """Test getting all items when none exist."""
        response = client.get('/items', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert data['items'] == []

    def test_get_all_items(self, client, db, sample_item, sample_store, auth_headers):
        """Test getting all items."""
        # Create additional item
        item2 = ItemModel(name='Item 2', price=29.99, store_id=sample_store.id)
        item2.save_to_db()

        response = client.get('/items', headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert len(data['items']) == 2
        item_names = [i['name'] for i in data['items']]
        assert 'Test Item' in item_names
        assert 'Item 2' in item_names

    def test_get_all_items_unauthenticated(self, client, db):
        """Test getting all items without authentication."""
        response = client.get('/items')

        assert response.status_code == 401
