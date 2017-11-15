from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Section 6
class Item(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')

    @jwt_required()  # Requires dat token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):

        # Overwrite current Items list with new list except the deleted
        # Must use global keyword to change variable from private to global
        try:
            ItemModel.remove(name)
            return {'message': '{} deleted'.format(name)}, 201
        except:
            return {"message": "There's been a problem deleting, exiting"}, 500

            # return {'message': 'item not deleted, does not exist'}

    @jwt_required()
    def put(self, name):
        # Create or Update
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        update_item = ItemModel(name,data['price'])

        if item is None:
            try:
                update_item.insert()
            except:
                return {"message": "an error occured on insert"}, 500

        else:
            update_item.update()

        return update_item.json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return ItemModel.retreiveMany()


