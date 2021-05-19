from flask_restful import reqparse, Resource
from models.users import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    def post(self):
        args = UserRegister.parser.parse_args()
        if User.find_by_username(args['username']):
            return f"user {args['username']} already exists"
        user = User(**args)
        user.add_user()

        return user.json(), 400
