from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_jwt import JWT, jwt_required, current_identity
import sqlite3

parser = reqparse.RequestParser()
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data1.db')
        cur = con.cursor()


        query = 'SELECT * FROM users WHERE username = ?'
        row = cur.execute(query, (username,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(id):
        con = sqlite3.connect('data1.db')
        cur = con.cursor()

        query = 'SELECT * FROM users WHERE id = ?'
        row = cur.execute(query, (id,)).fetchone()

        con.close()

        user = User(*row) if row else None
        return user

class UserRegister(Resource):
    def post(self):
        connection = sqlite3.connect('data1.db')
        cursor = connection.cursor()
        parser.add_argument('username', help="Username can't be blank")
        parser.add_argument('password', help="Password can't be blank")
        args = parser.parse_args()
        if list(cursor.execute("SELECT * FROM users WHERE username = '%s'" %args['username'])) != []:
            abort(404, message="Username {} already exists.".format(args['username']))
        else:
            query = 'INSERT INTO users(id, username, password) VALUES (NULL, ?, ?)'
            user = (args['username'], args['password'])
            cursor.execute(query, user)
            connection.commit()
            connection.close()
            return "Successfuly added user {}".format(args['username']), 201