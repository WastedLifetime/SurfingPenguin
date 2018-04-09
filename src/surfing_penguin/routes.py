"""routes.py: Each function in this file indicates a web page (HTML page)."""

from surfing_penguin import surfing_penguin, api, login_manager
from flask_restplus import Resource, fields
from surfing_penguin.db_interface import UserFunctions
from flask_login import login_user, logout_user, current_user, login_required


api_return_message = api.model("return_message_model", {
        'messages': fields.String
    })
api_get_user = api.model("get_user_model", {
        'username': fields.String,
        'password': fields.String,
    })


api_return_user = api.model("return_user_model", {
        'username': fields.String,
        'messages': fields.String,
    })


api_show_user = api.model("show_user_model", {
        'username': fields.String,
    })


api_show_user_and_time = api.model("show_user_and_time_model", {
        'username': fields.String,
        'last_seen': fields.DateTime
    })
""" user account associated APIs:
    register, login, show_users, delete_user, search_user """


@surfing_penguin.before_request
def before_request():
    # before each operation of a user, update his/her last_seen
    if current_user.is_authenticated:
        UserFunctions.update_last_seen(current_user.username)


@api.route('/hi')
class hi(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        if current_user.is_authenticated:
            return {'messages': "hi, {}!".format(current_user.username)}
        return {'messages': "hi, stranger!"}


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
    @api.marshal_with(api_return_message)
    @api.expect(api_get_user)
    def post(self):
        if current_user.is_authenticated:
            return {'messages': "You had logged in before."}
        name = api.payload['username']
        password = api.payload['password']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        if UserFunctions.check_password(name, password) is False:
            return {'messages': "wrong passwd"}
        user = UserFunctions.get_user(name)
        login_user(user)
        return {'messages': "Login: {}".format(name)}


@api.route('/logout')
class logout(Resource):
    @api.marshal_with(api_return_message)
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {'messages': "user logged out"}
        return {'messages': "You did not logged in"}


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
    @login_required
    def post(self):
        name = api.payload['username']
        if UserFunctions.search_user(name) is False:
            return {'messages': "user not found"}
        UserFunctions.delete_user(name)
        return {'messages': "user {} deleted".format(name)}


@api.route('/search_user')
class search_user(Resource):
    @api.marshal_with(api_show_user_and_time)
    @api.expect(api_show_user)
    def post(self):
        search_name = api.payload['username']
        if UserFunctions.search_user(search_name) is False:
            return {'messages': "user does not exist"}
        return UserFunctions.get_user(search_name)


@login_manager.unauthorized_handler
@api.marshal_with(api_return_message)
def unauthorized():
    # TODO: Flash this message somewhere.
    print("entering")
    return {'message': "Please Login First"}


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
