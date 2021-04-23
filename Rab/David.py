from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

from werkzeug.security import safe_str_cmp


products = []


class Item(Resource):


    def get(self, name):
        product = list(filter(lambda i: i['name'] == name, products))
        if product:
            return jsonify(product[0])
        raise Error('Product "{}" does not exist.'.format(name), status_code=404)


    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, location='form', help='Invalid price value')
        price = parser.parse_args()['price']
        if not price:
            raise Error('Please specify product price.')
        new_product = {'name': name, 'price': price}
        if list(filter(lambda i: i['name'] == name, products)):
            raise Error('Product "{}" is already in the shop. Use PUT request to edit it.'.format(name))
        products.append(new_product)
        return jsonify(new_product)


    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, help='Invalid price value')
        price = parser.parse_args()['price']
        if not price:
            raise Error('Please specify price value.')
        product = {'name': name, 'price': price}
        try:
            index = products.index(list(filter(lambda i: i['name'] == name, products))[0])
            products[index]['price'] = price
        except IndexError:
            products.append(product)
        return jsonify(product)


    def delete(self, name):
        product = list(filter(lambda i: i['name'] == name, products))
        if product:
            products.pop(product.index(product[0]))
            return '', 204
        raise Error('Product "{}" does not exist.'.format(name), status_code=404)


class ItemList(Resource):

    def get(self):
        return jsonify({'items': products})


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=list, help='Invalid product data')
        new_items = eval(''.join(parser.parse_args()['items']))
        if new_items:
            products.extend(new_items)
            return jsonify({'items': products})
        raise Error('Please specify new items in the body.')


class Error(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'status_code': self.status_code, 'message': self.message}


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f"User(id=){self.id}"


users = [
    User(1, 'Daoortor', '1234543212'),
    User(2, 'Mthd', 'correcthorsebatterystaple')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "FD"


@app.errorhandler(Error)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response









api.add_resource(Item, '/product/<string:name>')
api.add_resource(ItemList, '/')

if __name__ == '__main__':
    app.run(debug=True, port=9999)