#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for database models."""

import pytest
from app.models.user import UserModel
from app.models.item import ItemModel
from app.models.store import StoreModel


class TestUserModel:
    """Tests for UserModel."""

    def test_create_user(self, db):
        """Test creating a user."""
        user = UserModel(username='testuser', password='testpass')
        db.session.add(user)
        db.session.commit()

        assert user.id is not None
        assert user.username == 'testuser'
        assert user.password == 'testpass'

    def test_find_by_username(self, db, sample_user):
        """Test finding user by username."""
        user = UserModel.find_by_username('sampleuser')
        assert user is not None
        assert user.username == 'sampleuser'

    def test_find_by_username_not_found(self, db):
        """Test finding non-existent user."""
        user = UserModel.find_by_username('nonexistent')
        assert user is None

    def test_find_by_id(self, db, sample_user):
        """Test finding user by ID."""
        user = UserModel.find_by_id(sample_user.id)
        assert user is not None
        assert user.id == sample_user.id

    def test_find_by_id_not_found(self, db):
        """Test finding user by non-existent ID."""
        user = UserModel.find_by_id(999)
        assert user is None

    def test_save_to_db(self, db):
        """Test saving user to database."""
        user = UserModel(username='newuser', password='newpass')
        user.save_to_db()

        saved_user = UserModel.find_by_username('newuser')
        assert saved_user is not None
        assert saved_user.username == 'newuser'

    def test_check_password(self, db, sample_user):
        """Test password checking."""
        assert sample_user.check_password('samplepass') is True
        assert sample_user.check_password('wrongpass') is False


class TestStoreModel:
    """Tests for StoreModel."""

    def test_create_store(self, db):
        """Test creating a store."""
        store = StoreModel(name='Test Store')
        db.session.add(store)
        db.session.commit()

        assert store.id is not None
        assert store.name == 'Test Store'

    def test_find_by_name(self, db, sample_store):
        """Test finding store by name."""
        store = StoreModel.find_by_name('Test Store')
        assert store is not None
        assert store.name == 'Test Store'

    def test_find_by_name_not_found(self, db):
        """Test finding non-existent store."""
        store = StoreModel.find_by_name('nonexistent')
        assert store is None

    def test_save_to_db(self, db):
        """Test saving store to database."""
        store = StoreModel(name='New Store')
        store.save_to_db()

        saved_store = StoreModel.find_by_name('New Store')
        assert saved_store is not None
        assert saved_store.name == 'New Store'

    def test_delete_from_db(self, db, sample_store):
        """Test deleting store from database."""
        store_id = sample_store.id
        sample_store.delete_from_db()

        deleted_store = StoreModel.query.filter_by(id=store_id).first()
        assert deleted_store is None

    def test_json(self, db, sample_store, sample_item):
        """Test store JSON representation."""
        json_data = sample_store.json()
        assert json_data['name'] == 'Test Store'
        assert 'items' in json_data
        assert len(json_data['items']) == 1
        assert json_data['items'][0]['name'] == 'Test Item'

    def test_json_empty_items(self, db):
        """Test store JSON with no items."""
        store = StoreModel(name='Empty Store')
        db.session.add(store)
        db.session.commit()

        json_data = store.json()
        assert json_data['name'] == 'Empty Store'
        assert json_data['items'] == []


class TestItemModel:
    """Tests for ItemModel."""

    def test_create_item(self, db, sample_store):
        """Test creating an item."""
        item = ItemModel(name='Test Item', price=19.99, store_id=sample_store.id)
        db.session.add(item)
        db.session.commit()

        assert item.id is not None
        assert item.name == 'Test Item'
        assert item.price == 19.99
        assert item.store_id == sample_store.id

    def test_find_by_name(self, db, sample_item):
        """Test finding item by name."""
        item = ItemModel.find_by_name('Test Item')
        assert item is not None
        assert item.name == 'Test Item'
        assert item.price == 19.99

    def test_find_by_name_not_found(self, db):
        """Test finding non-existent item."""
        item = ItemModel.find_by_name('nonexistent')
        assert item is None

    def test_save_to_db(self, db, sample_store):
        """Test saving item to database."""
        item = ItemModel(name='New Item', price=29.99, store_id=sample_store.id)
        item.save_to_db()

        saved_item = ItemModel.find_by_name('New Item')
        assert saved_item is not None
        assert saved_item.name == 'New Item'
        assert saved_item.price == 29.99

    def test_delete_from_db(self, db, sample_item):
        """Test deleting item from database."""
        item_id = sample_item.id
        sample_item.delete_from_db()

        deleted_item = ItemModel.query.filter_by(id=item_id).first()
        assert deleted_item is None

    def test_json(self, db, sample_item, sample_store):
        """Test item JSON representation."""
        json_data = sample_item.json()
        assert json_data['name'] == 'Test Item'
        assert json_data['price'] == 19.99
        assert json_data['store_id'] == sample_store.id

    def test_relationship_with_store(self, db, sample_item, sample_store):
        """Test item-store relationship."""
        assert sample_item.store is not None
        assert sample_item.store.id == sample_store.id
        assert sample_item.store.name == 'Test Store'
