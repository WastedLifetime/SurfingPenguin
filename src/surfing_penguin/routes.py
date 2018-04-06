"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import api
from flask_restplus import Resource, fields
from surfing_penguin.db_interface import UserFunctions

question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
    })


api_get_user = api.model("get_user_model", {
        'username': fields.String,
        'id': fields.Integer,
        'password': fields.String,
    })


api_return_user = api.model("return_user_model", {
        'username': fields.String,
        'id': fields.Integer,
        'messages': fields.String,
    })


api_show_user = api.model("show_user_model", {
        'username': fields.String,
        'id': fields.Integer,
    })

""" user account associated APIs:
    register, login, show_users, delete_user, search_user """


@api.route('/register')
class register(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is True:
            return {'messages': "use another name"}
        return UserFunctions.register(name, password)


@api.route('/login')
class login(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        if UserFunctions.check_password(name, password) is False:
            return {'messages': "wrong passwd"}
        return {'messages': "Login: {}".format(name)}


@api.route('/show_users')
class show_users(Resource):
    @api.marshal_list_with(api_show_user)
    def get(self):
        users = UserFunctions.get_all_users()
        return users


@api.route('/delete_user')
class delete_user(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        UserFunctions.delete_user(name)
        return {'messages': "user {} deleted".format(name)}


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user)
    @api.expect(api_show_user)
    def post(self):
        search_name = api.payload['username']
        if UserFunctions.search_user(search_name) is False:
            return {'messages': "user does not exist"}
        return UserFunctions.get_user(search_name)


def convert_user_to_json(user):
    json_user = {
        "username": user.username,
        "register_time": user.register_time.isoformat(),
        "last_login": user.last_login.isoformat()
    }
    return json_user


def convert_users_to_json(users):
    json_users = []
    for user in users:
        json_users.append(convert_user_to_json(user))
    return json_users
