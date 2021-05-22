from flask_restful import Api
from flask import Flask
from flask_jwt import JWT
from security import authenticate, identity
from resources.items import Item, ItemList
from resources.users import UserRegister
from create_tables import createtables
from db import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data4.db'
app.config['SECRET_KEY'] = 'super-secret'
db.init_app(app)
createtables()

jwt = JWT(app, authenticate, identity)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<name>')
api.add_resource(UserRegister, '/register')

app.run(debug=True)
