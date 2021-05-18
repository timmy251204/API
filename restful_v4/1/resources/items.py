import sqlite3
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
from models.items import Items


class Item(Resource):
    @jwt_required()
    def get(self, name):
        if Items.get_item(name):
            item = Items.get_item(name)
            return item.json()
        else:
            return f"item {name} doesn`t exist"

    @jwt_required()
    def delete(self, name):
        if Items.get_item(name):
            item = Items.get_item(name)
            item.delete_item()
            return '', 204
        else:
            return f"item {name} doesn`t exist"

    @jwt_required()
    def post(self, name):
        if Items.get_item(name):
            return f"item {name} already exists"
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
        args = parser.parse_args()
        argsfull = {'name': name, 'price': args['price']}
        item = Items(**argsfull)
        item.add_item()
        return item.json(), 201

    @jwt_required()
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help="Price cannot be blank!")
        args = parser.parse_args()
        if Items.get_item(name):
            item = Items.get_item(name)
            item.price = args['price']
            item.update_item()
            return item.json(), 201
        argsfull = {'name': name, 'price': args['price']}
        item = Items(**argsfull)
        item.add_item()
        return item.json(), 201


# itemlist resource
class ItemList(Resource):

    @jwt_required()
    def get(self):
        items = Items.get_all()
        itemtrue = []
        for item in items:
            itemtrue.append(item.json())
        return itemtrue

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=dict, action='append', help="Name cannot be blank!")
        args = parser.parse_args()
        added = []
        for i in range(len(args['items'])):
            if Items.get_item(args['items'][i]['name']):
                return "Item {} already exists".format(args['items'][i]['name'])
            else:
                trueargs = {'name': args['items'][i]['name'], 'price': args['items'][i]['price']}
                item = Items(**trueargs)
                item.add_item()
                added.append(trueargs)
        return added, 201
