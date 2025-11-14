#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.item import ItemModel
from app.util.logz import create_logger

item_bp = Blueprint('item', __name__)
logger = create_logger()


@item_bp.route('/item/<string:name>', methods=['GET'])
@jwt_required()
def get_item(name):
    """Get an item by name."""
    item = ItemModel.find_by_name(name)
    if item:
        logger.info(f'returning item: {item.json()}')
        return jsonify(item.json())
    return jsonify({'message': 'Item not found'}), 404


@item_bp.route('/item/<string:name>', methods=['POST'])
@jwt_required()
def create_item(name):
    """Create a new item."""
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate required fields
    if 'price' not in data:
        return jsonify({'message': 'price field cannot be left blank'}), 400
    if 'store_id' not in data:
        return jsonify({'message': 'Must enter the store id'}), 400

    logger.info(f'parsed data: {data}')

    if ItemModel.find_by_name(name):
        return jsonify({'message': f"An item with name '{name}' already exists."}), 400

    try:
        price = float(data['price'])
        store_id = int(data['store_id'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid data types for price or store_id'}), 400

    item = ItemModel(name, price, store_id)

    try:
        item.save_to_db()
    except Exception as e:
        logger.error(f'Error inserting item: {e}')
        return jsonify({"message": "An error occurred inserting the item."}), 500

    return jsonify(item.json()), 201


@item_bp.route('/item/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_item(name):
    """Delete an item by name."""
    item = ItemModel.find_by_name(name)
    if item:
        item.delete_from_db()

    return jsonify({'message': 'item has been deleted'})


@item_bp.route('/item/<string:name>', methods=['PUT'])
@jwt_required()
def update_item(name):
    """Create or update an item."""
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate required fields
    if 'price' not in data:
        return jsonify({'message': 'price field cannot be left blank'}), 400
    if 'store_id' not in data:
        return jsonify({'message': 'Must enter the store id'}), 400

    try:
        price = float(data['price'])
        store_id = int(data['store_id'])
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid data types for price or store_id'}), 400

    item = ItemModel.find_by_name(name)

    if item is None:
        item = ItemModel(name, price, store_id)
    else:
        item.price = price

    item.save_to_db()

    return jsonify(item.json())


@item_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    """Get all items."""
    return jsonify({'items': [item.json() for item in ItemModel.query.all()]})
