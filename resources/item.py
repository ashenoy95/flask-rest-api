from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id!')


    @jwt_required()	# authenticate before calling get()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400

        payload = Item.parser.parse_args()
        item = ItemModel(name, **payload)
        try:
            item.upsert()
        except:
            return {'message': 'Error occured while inserting.'}, 500   # internal server error

        return item.json(), 201	

    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete() 
            return {'message': 'Item deleted.'}


    def put(self, name):
        payload = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **payload)
        else:
            item.price = payload['price']
            item.store_id = payload['store_id']
        item.upsert()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}