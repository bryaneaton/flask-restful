#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Blueprint, request, jsonify
from app.models.store import StoreModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger

store_bp = Blueprint('store', __name__)
logger = create_logger()


@store_bp.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    """Get a store by name."""
    store = StoreModel.find_by_name(name)
    if store:
        return jsonify(store.json())
    return jsonify({'message': 'Store not found'}), 404


@store_bp.route('/store/<string:name>', methods=['POST'])
@jwt_required()
def create_store(name):
    """Create a new store."""
    if StoreModel.find_by_name(name):
        return jsonify({'message': f"A store with name '{name}' already exists."}), 400

    store = StoreModel(name)
    try:
        store.save_to_db()
    except Exception as e:
        logger.error(f'Error creating store: {e}')
        return jsonify({"message": "An error occurred creating the store."}), 500

    return jsonify(store.json()), 201


@store_bp.route('/store/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_store(name):
    """Delete a store by name."""
    store = StoreModel.find_by_name(name)
    if store:
        store.delete_from_db()

    return jsonify({'message': 'Store deleted'})


@store_bp.route('/stores', methods=['GET'])
def get_stores():
    """Get all stores."""
    return jsonify({'stores': [store.json() for store in StoreModel.query.all()]})
