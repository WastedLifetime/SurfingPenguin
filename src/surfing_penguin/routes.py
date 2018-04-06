"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import api, auth
from flask import request, g
from flask_restplus import Resource, fields
from surfing_penguin.db_interface import UserFunctions
from surfing_penguin.models import User
from functools import wraps

api_return_message = api.model("return_message", {
        'message': fields.String
    })


api_token = api.model("api_token", {
        'token': fields.String,
        'duration': fields.Integer
    })


question = api.model("question_model", {
        'content': fields.String,
        'id': fields.Integer
    })


api_get_user = api.model("get_user_model", {
        'username': fields.String,
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


# TODO:combine it with HTTPauth
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message': 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message': 'Your token is wrong, wrong, wrong!!!'}, 401

        return f(*args, **kwargs)

    return decorated


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = UserFunctions.get_user(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@api.route('/api_token')
class api_token(Resource):
    @auth.login_required
    @api.marshal_with(api_token)
    def get(self):
        token = g.user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}


@api.route('/api_resource')
class api_resource(Resource):
    @auth.login_required
    @api.marshal_with(api_return_message)
    def get(self):
        return {'message': 'hi, user {}'.format(g.user.username)}


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


# TODO: combine this with HTTPauth
@api.route('/login')
class login(Resource):
    @api.marshal_with(api_return_user)
    @api.expect(api_get_user)
    def post(self):
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        user = UserFunctions.get_user(name)
        if user.verify_password(password) is False:
            return {'messages': "wrong passwd"}
        return {'username': name, 'messages': "Login: {}".format(name)}


@api.route('/logout')
class logout(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        return {'message': 'user logout'}


@api.route('/show_users')
class show_users(Resource):
    @api.marshal_list_with(api_show_user)
    def get(self):
        users = UserFunctions.get_all_users()
        return users


@api.route('/delete_user')
class delete_user(Resource):
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    # @api.doc(security='apikey')
    # @token_required
    @auth.login_required
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
