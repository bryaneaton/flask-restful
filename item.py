import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        select_items = 'select * from items where name = ?'

        cursor = connection.cursor()
        result = cursor.execute(select_items, (name,))  # Single value Tuple
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}

    # @jwt_required()  # Requires dat token
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    # @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "Insert into items (name, price) values (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        # Overwrite current Items list with new list except the deleted
        # Must use global keyword to change variable from private to global

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "delete from items where name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': '{} deleted'.format(name)}
        # return {'message': 'item not deleted, does not exist'}

    # @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            # Create
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            # Update
            item.update(data)
        return item, 201


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'items': items}
