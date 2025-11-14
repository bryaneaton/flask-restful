#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for utility functions."""

import json
import logging
import pytest
from app.util.encoder import AlchemyEncoder
from app.util.logz import create_logger
from app.models.user import UserModel


class TestAlchemyEncoder:
    """Tests for AlchemyEncoder."""

    def test_encode_sqlalchemy_model(self, db, sample_user):
        """Test encoding SQLAlchemy model to JSON."""
        json_str = json.dumps(sample_user, cls=AlchemyEncoder)
        data = json.loads(json_str)

        assert 'username' in data
        assert data['username'] == 'sampleuser'
        assert 'password' in data
        assert 'id' in data

    def test_encode_regular_object(self):
        """Test encoding regular Python objects."""
        regular_dict = {'key': 'value', 'number': 42}
        json_str = json.dumps(regular_dict, cls=AlchemyEncoder)
        data = json.loads(json_str)

        assert data['key'] == 'value'
        assert data['number'] == 42

    def test_encode_with_relationships(self, db, sample_item, sample_store):
        """Test encoding model with relationships."""
        json_str = json.dumps(sample_item, cls=AlchemyEncoder)
        data = json.loads(json_str)

        assert 'name' in data
        assert data['name'] == 'Test Item'
        assert 'price' in data
        assert 'store_id' in data


class TestCreateLogger:
    """Tests for create_logger function."""

    def test_create_logger_returns_logger(self):
        """Test that create_logger returns a logger instance."""
        logger = create_logger()
        assert logger is not None
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self):
        """Test logger has correct name."""
        logger = create_logger()
        assert logger.name == 'rich'

    def test_logger_has_handlers(self):
        """Test logger has handlers configured."""
        logger = create_logger()
        # The logger should have handlers from basicConfig
        root_logger = logging.getLogger()
        assert len(root_logger.handlers) > 0

    def test_logger_can_log(self, caplog):
        """Test that logger can actually log messages."""
        logger = create_logger()
        with caplog.at_level(logging.INFO):
            logger.info('Test message')

        # Check that something was logged
        assert len(caplog.records) > 0
