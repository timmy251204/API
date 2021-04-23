from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
app = Flask(__name__)
api = Api(app)

ITEMS = [
        {
            'name': 'chair',
            'price': 1500,
        }

]

class main(Resource):
    def get(self):
        return {'hello': 'world'}

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
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
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()



def abort_if_name_doesnt_exist(name):
    if list(filter(lambda item: item['name'] == name, ITEMS)) == [] :
        return abort(404, message="name {} doesn't exist".format(name))

def abort_if_name_already_exist(name):
    if list(filter(lambda item: item['name'] == name, ITEMS)) != []:
        return abort(404,  message="name {} already exist".format(name))


parser = reqparse.RequestParser()
parser.add_argument('price')
parser.add_argument('items', type=dict, action="append")


class Item(Resource):
    def get(self, name):
        abort_if_name_doesnt_exist(name)
        item = list(filter(lambda item: item['name'] == name, ITEMS))
        return item

    def post(self, name):
        abort_if_name_already_exist(name)
        args = parser.parse_args()
        ITEMS.append({'name': name, 'price': args['price']})
        return ITEMS[-1], 201

    def put(self, name):
        abort_if_name_doesnt_exist(name)
        args = parser.parse_args()
        item = {'name': name, 'price': args['price']}
        if list(filter(lambda item: item['name'] == name, ITEMS)) == []:
            ITEMS.append({'name': name, 'price': args['price']})
        else:
            ITEMS[ITEMS.index(*list(filter(lambda item: item['name'] == name, ITEMS)))] = item
        return item, 201

    def delete(self, name):
        abort_if_name_doesnt_exist(name)
        del ITEMS[ITEMS.index(*list(filter(lambda item: item['name'] == name, ITEMS)))]
        return '', 204


class ItemList(Resource):

    def get(self):
        return ITEMS

    def post(self):
        args = parser.parse_args()
        for i in range(len(args['items'])):
            abort_if_name_already_exist(args['items'][i]['name'])
            ITEMS.append(args['items'][i])
        return "Successfully added items {}".format(args['items']), 201









api.add_resource(Item, '/items/<name>')
api.add_resource(main, '/')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)