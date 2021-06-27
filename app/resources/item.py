#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.item import ItemModel
from app.util.logz import create_logger


class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True,
                        help='Must enter the store id')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires dat token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        self.logger.info(f'returning item: {item.json()}')
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        self.logger.info(f'parsed args: {Item.parser.parse_args()}')

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(
                name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

            return {'message': 'item has been deleted'}

    @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {
            'items': [item.json() for item in ItemModel.query.all()]}  # More pythonic
        ##return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #Alternate Lambda way
