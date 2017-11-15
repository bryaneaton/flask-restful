import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        select_items = 'select name, price from items where name = ?'

        cursor = connection.cursor()
        result = cursor.execute(select_items, (name,))  # Single value Tuple
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

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

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item, 201

        # @jwt_required()
    def delete(self, name):

            # Overwrite current Items list with new list except the deleted
            # Must use global keyword to change variable from private to global
        try:
            self.remove(name)
            return {'message': '{} deleted'.format(name)}, 201
        except:
            return {"message": "There's been a problem deleting, exiting"}, 500

        # return {'message': 'item not deleted, does not exist'}

    # @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        update_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(update_item)
            except:
                return {"message": "an error occured on insert"}, 500

        else:
            self.update(update_item)

        return item, 201
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items (price, name) Values(?,?)"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "update items set price = ? where name = ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @classmethod
    def remove(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "delete from items where name = ?"
        cursor.execute(query, (item,))

        connection.commit()
        connection.close()



class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return self.retreiveMany()

    @classmethod
    def retreiveMany(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select name, price from items"
        result = cursor.execute(query)

        # TODO: retreive item list
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        connection.close()

        return {'items': items}
